import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
import xgboost as xgb

def model(dbt, session):
    # Load feature table
    df = session.execute('SELECT * FROM nasa_rul_features').fetchdf()

    # Features and target
    target = 'rul_target'
    features = [
        'vibration',
        'vibration_roll_mean_5',
        'vibration_roll_std_5',
        'vibration_lag_1',
        'vibration_lag_2',
        'vibration_slope_1',
        'quality',
    ]

    # Drop rows with nulls (from lag/rolling at start of each unit)
    df = df.dropna(subset=features + [target])

    # Train/test split: last 20% cycles per unit for test, rest for train
    def split_train_test(df, unit_col='unit_number', cycle_col='cycle', test_frac=0.2):
        train_idx = []
        test_idx = []
        for unit in df[unit_col].unique():
            unit_df = df[df[unit_col] == unit]
            cutoff = int(len(unit_df) * (1 - test_frac))
            train_idx += list(unit_df.index[:cutoff])
            test_idx += list(unit_df.index[cutoff:])
        return df.loc[train_idx], df.loc[test_idx]

    train_df, test_df = split_train_test(df)

    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    y_test = test_df[target]

    # --- Enhanced Random Forest: Hyperparameter Tuning, Feature Importance, Diagnostics ---
    from sklearn.model_selection import RandomizedSearchCV
    import warnings
    warnings.filterwarnings('ignore')

    rf_param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 5, 10, 20],
        'max_features': ['auto', 'sqrt', 0.5],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }
    rf_base = RandomForestRegressor(random_state=42)
    rf_search = RandomizedSearchCV(
        rf_base, rf_param_grid, n_iter=10, scoring='neg_root_mean_squared_error',
        cv=3, random_state=42, n_jobs=-1, verbose=0
    )
    rf_search.fit(X_train, y_train)
    rf = rf_search.best_estimator_
    rf_preds = rf.predict(X_test)
    try:
        rf_rmse = mean_squared_error(y_test, rf_preds, squared=False)
    except TypeError:
        rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
    # Feature importance
    rf_feature_importance = pd.DataFrame({
        'feature': features,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    # Save feature importances to DuckDB for traceability
    session.execute('DROP TABLE IF EXISTS rf_feature_importance')
    session.execute('CREATE TABLE rf_feature_importance (feature VARCHAR, importance DOUBLE)')
    for _, row in rf_feature_importance.iterrows():
        session.execute('INSERT INTO rf_feature_importance VALUES (?, ?)', (row['feature'], float(row['importance'])))
    # Diagnostics: OOB score if available
    rf_oob = getattr(rf, 'oob_score_', None)
    results = []
    results.append({'model_name': 'RandomForestRegressor', 'rmse': rf_rmse, 'oob_score': rf_oob, 'best_params': str(rf_search.best_params_)})


    # --- Enhanced Linear Regression: Scaling, Regularization, Poly Features, Diagnostics ---
    from sklearn.preprocessing import StandardScaler, PolynomialFeatures
    from sklearn.linear_model import Ridge, Lasso, ElasticNet
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    import statsmodels.api as sm

    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Multicollinearity check (VIF)
    vif_data = pd.DataFrame()
    vif_data['feature'] = features
    vif_data['VIF'] = [variance_inflation_factor(X_train_scaled, i) for i in range(X_train_scaled.shape[1])]
    session.execute('DROP TABLE IF EXISTS lr_vif')
    session.execute('CREATE TABLE lr_vif (feature VARCHAR, vif DOUBLE)')
    for _, row in vif_data.iterrows():
        session.execute('INSERT INTO lr_vif VALUES (?, ?)', (row['feature'], float(row['VIF'])))

    # Polynomial features (degree=2)
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_train_poly = poly.fit_transform(X_train_scaled)
    X_test_poly = poly.transform(X_test_scaled)
    poly_features = poly.get_feature_names_out(features)

    # Linear Regression (vanilla)
    lr = LinearRegression()
    lr.fit(X_train_poly, y_train)
    lr_preds = lr.predict(X_test_poly)
    try:
        lr_rmse = mean_squared_error(y_test, lr_preds, squared=False)
    except TypeError:
        lr_rmse = np.sqrt(mean_squared_error(y_test, lr_preds))

    # Ridge Regression
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train_poly, y_train)
    ridge_preds = ridge.predict(X_test_poly)
    try:
        ridge_rmse = mean_squared_error(y_test, ridge_preds, squared=False)
    except TypeError:
        ridge_rmse = np.sqrt(mean_squared_error(y_test, ridge_preds))

    # Lasso Regression
    lasso = Lasso(alpha=0.1, max_iter=10000)
    lasso.fit(X_train_poly, y_train)
    lasso_preds = lasso.predict(X_test_poly)
    try:
        lasso_rmse = mean_squared_error(y_test, lasso_preds, squared=False)
    except TypeError:
        lasso_rmse = np.sqrt(mean_squared_error(y_test, lasso_preds))

    # ElasticNet
    enet = ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=10000)
    enet.fit(X_train_poly, y_train)
    enet_preds = enet.predict(X_test_poly)
    try:
        enet_rmse = mean_squared_error(y_test, enet_preds, squared=False)
    except TypeError:
        enet_rmse = np.sqrt(mean_squared_error(y_test, enet_preds))

    # Residual diagnostics (vanilla LR)
    residuals = y_test - lr_preds
    # Homoscedasticity: plot or test (Breusch-Pagan, not shown here)
    # Normality: Shapiro-Wilk or Q-Q plot (not shown here)
    # Autocorrelation: Durbin-Watson
    dw_stat = sm.stats.stattools.durbin_watson(residuals)
    session.execute('DROP TABLE IF EXISTS lr_diagnostics')
    session.execute('CREATE TABLE lr_diagnostics (metric VARCHAR, value DOUBLE)')
    session.execute('INSERT INTO lr_diagnostics VALUES (?, ?)', ('durbin_watson', float(dw_stat)))

    # Store all RMSEs for model selection
    results.append({'model_name': 'LinearRegression', 'rmse': lr_rmse, 'variant': 'vanilla'})
    results.append({'model_name': 'Ridge', 'rmse': ridge_rmse, 'variant': 'ridge'})
    results.append({'model_name': 'Lasso', 'rmse': lasso_rmse, 'variant': 'lasso'})
    results.append({'model_name': 'ElasticNet', 'rmse': enet_rmse, 'variant': 'elasticnet'})


    # --- Enhanced XGBoost: Hyperparameter Tuning, Early Stopping, SHAP, CV ---
    from sklearn.model_selection import RandomizedSearchCV, KFold
    import shap

    xgb_param_grid = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'max_depth': [3, 5, 7, 10],
        'min_child_weight': [1, 3, 5],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'gamma': [0, 0.1, 0.2],
        'reg_alpha': [0, 0.1, 1],
        'reg_lambda': [1, 1.5, 2]
    }
    xgb_base = xgb.XGBRegressor(random_state=42, verbosity=0)
    xgb_search = RandomizedSearchCV(
        xgb_base, xgb_param_grid, n_iter=10, scoring='neg_root_mean_squared_error',
        cv=3, random_state=42, n_jobs=-1, verbose=0
    )
    xgb_search.fit(X_train, y_train, early_stopping_rounds=10, eval_set=[(X_test, y_test)], verbose=False)
    xgbr = xgb_search.best_estimator_
    xgb_preds = xgbr.predict(X_test)
    try:
        xgb_rmse = mean_squared_error(y_test, xgb_preds, squared=False)
    except TypeError:
        xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_preds))
    # Cross-validation RMSE
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = []
    for train_idx, val_idx in kf.split(X_train):
        xgbr_cv = xgb.XGBRegressor(**xgbr.get_params())
        xgbr_cv.fit(X_train[train_idx], y_train.iloc[train_idx])
        preds_cv = xgbr_cv.predict(X_train[val_idx])
        try:
            rmse_cv = mean_squared_error(y_train.iloc[val_idx], preds_cv, squared=False)
        except TypeError:
            rmse_cv = np.sqrt(mean_squared_error(y_train.iloc[val_idx], preds_cv))
        cv_scores.append(rmse_cv)
    xgb_cv_rmse = float(np.mean(cv_scores))
    # SHAP feature importance
    explainer = shap.Explainer(xgbr, X_train)
    shap_values = explainer(X_train)
    shap_importance = pd.DataFrame({
        'feature': features,
        'mean_abs_shap': np.abs(shap_values.values).mean(axis=0)
    }).sort_values('mean_abs_shap', ascending=False)
    session.execute('DROP TABLE IF EXISTS xgb_feature_importance')
    session.execute('CREATE TABLE xgb_feature_importance (feature VARCHAR, mean_abs_shap DOUBLE)')
    for _, row in shap_importance.iterrows():
        session.execute('INSERT INTO xgb_feature_importance VALUES (?, ?)', (row['feature'], float(row['mean_abs_shap'])))
    # Store XGBoost results
    results.append({'model_name': 'XGBoost', 'rmse': xgb_rmse, 'cv_rmse': xgb_cv_rmse, 'best_params': str(xgb_search.best_params_)})

    # Store model performance table
    perf_df = pd.DataFrame(results)
    perf_df['is_best'] = perf_df['rmse'] == perf_df['rmse'].min()
    perf_df['timestamp'] = pd.Timestamp.now()
    perf_df = perf_df[['model_name', 'rmse', 'is_best', 'timestamp']]
    # Write model_performance table using DuckDB SQL
    session.execute('DROP TABLE IF EXISTS model_performance')
    session.execute('CREATE TABLE model_performance (model_name VARCHAR, rmse DOUBLE, is_best BOOLEAN, timestamp TIMESTAMP)')
    for _, row in perf_df.iterrows():
        session.execute(
            'INSERT INTO model_performance VALUES (?, ?, ?, ?)',
            (row['model_name'], float(row['rmse']), bool(row['is_best']), row['timestamp'])
        )

    # Use best model for predictions (lowest RMSE)
    best_model = min(results, key=lambda x: x['rmse'])['model_name']
    if best_model == 'RandomForestRegressor':
        preds = rf_preds
    elif best_model == 'LinearRegression':
        preds = lr_preds
    else:
        preds = xgb_preds

    # --- Enhanced KMeans: Scaling, Profiling, Robust Labeling, Diagnostics ---
    from sklearn.preprocessing import StandardScaler
    scaler_km = StandardScaler()
    cluster_features = scaler_km.fit_transform(test_df[features])
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=20)
    clusters = kmeans.fit_predict(cluster_features)
    # Cluster profiling: mean/variance of features and RUL
    cluster_profiles = []
    for i in range(3):
        mask = clusters == i
        profile = {
            'cluster': int(i),
            'count': int(mask.sum()),
            'mean_rul': float(test_df.loc[mask, target].mean()),
            'std_rul': float(test_df.loc[mask, target].std())
        }
        for f in features:
            profile[f'_mean_{f}'] = float(test_df.loc[mask, f].mean())
            profile[f'_std_{f}'] = float(test_df.loc[mask, f].std())
        cluster_profiles.append(profile)
    # Assign cluster labels: Green/Yellow/Red by mean RUL (high=Green)
    mean_ruls = [p['mean_rul'] for p in cluster_profiles]
    order = np.argsort(mean_ruls)[::-1]
    label_map = {order[0]: 'Green', order[1]: 'Yellow', order[2]: 'Red'}
    cluster_labels = np.array([label_map[c] for c in clusters], dtype=object)
    # Store cluster diagnostics in DuckDB
    session.execute('DROP TABLE IF EXISTS kmeans_cluster_diagnostics')
    col_defs = ', '.join([f'{k} DOUBLE' for k in cluster_profiles[0] if k != 'cluster'] + ['cluster INTEGER'])
    session.execute(f'CREATE TABLE kmeans_cluster_diagnostics ({col_defs})')
    for profile in cluster_profiles:
        vals = [profile[k] for k in profile if k != 'cluster'] + [profile['cluster']]
        placeholders = ', '.join(['?'] * len(vals))
        session.execute(f'INSERT INTO kmeans_cluster_diagnostics VALUES ({placeholders})', tuple(vals))
    # Store predictions and cluster assignments in output DataFrame
    test_df = test_df.copy()
    test_df['rul_pred'] = preds
    test_df['model_used'] = best_model
    test_df['health_zone'] = cluster_labels

    return test_df
