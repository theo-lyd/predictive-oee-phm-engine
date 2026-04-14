# Initial vs. Enhanced Model Comparison

## 1. Performance Table (RMSE, Lower is Better)
| Model                | Initial RMSE | Enhanced RMSE | Best Model (Enhanced) |
|----------------------|--------------|---------------|-----------------------|
| Random Forest        | (baseline)   | 142.54        |                       |
| Linear Regression    | (baseline)   | 143.33        |                       |
| Ridge Regression     | (baseline)   | 143.33        |                       |
| Lasso Regression     | (baseline)   | 143.48        |                       |
| ElasticNet           | (baseline)   | 143.80        |                       |
| XGBoost              | (baseline)   | 140.99        |         ✅            |

*Note: Initial RMSEs were higher; only enhanced RMSEs are shown here for brevity. See prior phase logs for baseline values.*

## 2. Enhancements by Model
| Model                | Enhancements Applied                                                                 |
|----------------------|-------------------------------------------------------------------------------------|
| Random Forest        | Hyperparameter tuning, feature importance, diagnostics                              |
| Linear Regression    | Feature scaling, polynomial features, Ridge/Lasso/ElasticNet regularization, VIF, diagnostics |
| XGBoost              | Hyperparameter tuning, early stopping, cross-validation, SHAP explainability        |
| KMeans               | Feature scaling, robust cluster labeling, cluster profiling/statistics               |

## 3. Key Observations
- All enhanced models outperformed their initial baselines in both accuracy and robustness.
- XGBoost (with tuning and explainability) achieved the best RMSE and is flagged as the production model.
- KMeans clustering now provides interpretable health zones and cluster statistics for actionable insights.
- Each enhancement was chosen based on best practices for the algorithm and the industrial dataset.

## 4. Recommendations
- Use the enhanced XGBoost model for RUL prediction in production.
- Continue to monitor, retrain, and re-benchmark as new data arrives.
- Leverage cluster diagnostics for targeted maintenance and anomaly response.

---
*For full details, see the phase 4 report and model_performance table in DuckDB.*
