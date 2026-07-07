from backend.services.sheets_service import get_feedback_data
from backend.services.data_processor import DataProcessor
from backend.services.charts_service import ChartService


feedback = get_feedback_data()

processor = DataProcessor(feedback)

summary = processor.build_summary()

charts = ChartService()

charts.generate_all_charts(summary)

print("✅ All charts generated successfully!")