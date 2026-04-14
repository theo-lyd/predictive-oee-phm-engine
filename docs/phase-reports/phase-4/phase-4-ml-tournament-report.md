## 7. Initial vs. Enhanced Model Comparison

For a detailed, side-by-side comparison of initial (baseline) and enhanced model results, as well as a summary of enhancements applied to each algorithm, see:

- [Phase 4 Initial vs. Enhanced Comparison](phase-4-initial-vs-enhanced-comparison.md)

### Highlights
- Enhanced models (with tuning, scaling, diagnostics, and explainability) achieved lower RMSE and greater robustness than initial baselines.
- XGBoost is the best-performing model for RUL prediction.
- KMeans clustering now provides actionable health zones and cluster statistics.
# Phase 4: ML Tournament & Segmentation Report

## 1. Overview
This phase benchmarks and enhances Random Forest, Linear Regression, and XGBoost for Remaining Useful Life (RUL) prediction, and implements KMeans clustering for anomaly segmentation. All enhancements are documented and results compared to initial baselines.

## 2. Model Benchmarking Results
- **Random Forest, Linear Regression, XGBoost**: All models were tuned and evaluated using RMSE. The best model is flagged in the `model_performance` table.
- **Enhancements**: Hyperparameter tuning, scaling, regularization, cross-validation, and SHAP explainability were applied as appropriate for each model.
- **Outcome**: Enhanced models achieved lower RMSE and improved robustness compared to initial baselines.

## 3. KMeans Clustering & Health Zones
- **Clustering**: KMeans with feature scaling segments assets into three health zones (Green/Yellow/Red) based on RUL and sensor features.
- **Diagnostics**: Cluster statistics (mean/std of RUL and features) are stored in `kmeans_cluster_diagnostics` for interpretability.

## 4. Key Learnings
- Model enhancements are justified for this industrial dataset: tuning, scaling, and diagnostics improved both accuracy and explainability.
- Not all enhancements are equally critical for every algorithm, but all contribute to a robust, production-ready solution.

## 5. Artifacts Delivered
- `model_performance` (RMSEs, best model)
- `rf_feature_importance`, `xgb_feature_importance`, `lr_vif`, `lr_diagnostics`
- `kmeans_cluster_diagnostics` (cluster profiles)

## 6. Next Steps
- Integrate results into the Maintenance Copilot and dashboards.
- Continue monitoring and retraining as new data arrives.
