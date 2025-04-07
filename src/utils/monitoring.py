import os
import time
import threading
import logging
import psutil
from utils.logging_config import configure_logging
from prometheus_client import start_http_server, Counter, Gauge, Histogram, Summary

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RegressionMonitor:
    def __init__(self, port=8002):
        self.port = port
        self.is_running = False
        self.v1_train_mse = Gauge('v1_train_mse', 'Train - MSE')
        self.v1_train_rmse = Gauge('v1_train_rmse', 'Train - RMSE')
        self.v1_train_mae = Gauge('v1_train_mae', 'Train - MAE')
        self.v1_train_r_squared = Gauge('v1_train_r2', 'Train - R² Score')
        self.v1_train_adj_r_squared = Gauge('v1_train_adj_r2', ' Train - Adjusted R² Score')
        self.v1_test_mse = Gauge('v1_test_mse', 'Test - MSE')
        self.v1_test_rmse = Gauge('v1_test_rmse', 'Test - RMSE')
        self.v1_test_mae = Gauge('v1_test_mae', 'Test - MAE')
        self.v1_test_r_squared = Gauge('v1_test_r2', 'Test - R² Score')
        self.v1_test_adj_r_squared = Gauge('v1_test_adj_r2', ' Test - Adjusted R² Score')

        self.v2_train_mse = Gauge('v2_train_mse', 'Train - MSE')
        self.v2_train_rmse = Gauge('v2_train_rmse', 'Train - RMSE')
        self.v2_train_mae = Gauge('v2_train_mae', 'Train - MAE')
        self.v2_train_r_squared = Gauge('v2_train_r2', 'Train - R² Score')
        self.v2_train_adj_r_squared = Gauge('v2_train_adj_r2', ' Train - Adjusted R² Score')
        self.v2_test_mse = Gauge('v2_test_mse', 'Test - MSE')
        self.v2_test_rmse = Gauge('v2_test_rmse', 'Test - RMSE')
        self.v2_test_mae = Gauge('v2_test_mae', 'Test - MAE')
        self.v2_test_r_squared = Gauge('v2_test_r2', 'Test - R² Score')
        self.v2_test_adj_r_squared = Gauge('v2_test_adj_r2', ' Test - Adjusted R² Score')

        self.memory_usage = Gauge('training_memory_usage_bytes', 'Memory usage of the training process')
        self.cpu_usage = Gauge('training_cpu_usage_percent', 'CPU usage percentage of the training process')

    def record_metrics(self, model='pr', type='test', mse=None, rmse=None, mae=None, r_squared=None, adj_r_squared=None):
        """Record regression metrics"""
        try:
            if model == 'pr':
                logger.info(f"Storing metrics for Polynomial Regression")
                if type != 'test':
                    if mse is not None:
                        self.v1_train_mse.set(mse)
                    if rmse is not None:
                        self.v1_train_rmse.set(rmse)
                    if mae is not None:
                        self.v1_train_mae.set(mae)
                    if r_squared is not None:
                        self.v1_train_r_squared.set(r_squared)
                    if adj_r_squared is not None:
                        self.v1_train_adj_r_squared.set(adj_r_squared)
                else:
                    if mse is not None:
                        self.v1_test_mse.set(mse)
                    if rmse is not None:
                        self.v1_test_rmse.set(rmse)
                    if mae is not None:
                        self.v1_test_mae.set(mae)
                    if r_squared is not None:
                        self.v1_test_r_squared.set(r_squared)
                    if adj_r_squared is not None:
                        self.v1_test_adj_r_squared.set(adj_r_squared)
            else:
                logger.info(f"Storing metrics for Decision Tree")
                if type != 'test':
                    if mse is not None:
                        self.v2_train_mse.set(mse)
                    if rmse is not None:
                        self.v2_train_rmse.set(rmse)
                    if mae is not None:
                        self.v2_train_mae.set(mae)
                    if r_squared is not None:
                        self.v2_train_r_squared.set(r_squared)
                    if adj_r_squared is not None:
                        self.v2_train_adj_r_squared.set(adj_r_squared)
                else:
                    if mse is not None:
                        self.v2_test_mse.set(mse)
                    if rmse is not None:
                        self.v2_test_rmse.set(rmse)
                    if mae is not None:
                        self.v2_test_mae.set(mae)
                    if r_squared is not None:
                        self.v2_test_r_squared.set(r_squared)
                    if adj_r_squared is not None:
                        self.v2_test_adj_r_squared.set(adj_r_squared)
        except Exception as e:
            logger.error(f"Error recording metrics for type={type}: {e}")

    def start(self):
        """Start the Prometheus HTTP server and resource monitoring thread"""
        try:
            start_http_server(self.port)
            logger.info(f"Prometheus metrics server started on port {self.port}")
            self.is_running = True
            self.monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
            self.monitor_thread.start()
            logger.info("Resource monitoring thread started")
            
            return True
        except Exception as e:
            logger.error(f"Failed to start monitoring: {e}")
            return False
    
    def stop(self):
        """Stop the resource monitoring thread"""
        self.is_running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2)
        logger.info("Resource monitoring stopped")

    def _monitor_resources(self):
            """Background thread to monitor system resources"""
            while self.is_running:
                try:
                    # Update CPU and memory metrics
                    process = psutil.Process(os.getpid())
                    self.memory_usage.set(process.memory_info().rss)
                    self.cpu_usage.set(process.cpu_percent(interval=0.1))               
                    time.sleep(5)  # Update every 5 seconds
                    
                except Exception as e:
                    logger.error(f"Error in resource monitoring thread: {e}")
                    time.sleep(30)  # Retry after a delay

def get_training_monitor(port=8002):
    """Get or create the training monitor singleton instance"""
    if not hasattr(get_training_monitor, 'instance'):
        get_training_monitor.instance = RegressionMonitor(port=port)
    return get_training_monitor.instance