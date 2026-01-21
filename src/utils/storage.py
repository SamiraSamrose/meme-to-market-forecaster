from google.cloud import storage
import json
import pandas as pd
from config.settings import PROJECT_ID, BUCKET_NAME

class StorageManager:
    def __init__(self):
        self.client = storage.Client(project=PROJECT_ID)
        self.bucket_name = BUCKET_NAME
        
    def export_to_gcs(self, data, filename):
        """Export dataframe to GCS as JSON"""
        
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(f"meme_market_outputs/{filename}")
            
            if isinstance(data, pd.DataFrame):
                json_data = data.to_json(orient='records', date_format='iso')
            else:
                json_data = json.dumps(data, indent=2)
            
            blob.upload_from_string(json_data, content_type='application/json')
            
            print(f"Exported {filename} to gs://{self.bucket_name}/meme_market_outputs/")
            return True
        except Exception as e:
            print(f"Export failed for {filename}: {str(e)}")
            return False
    
    def export_visual_metadata(self, metadata_list):
        """Export visual metadata for BigQuery integration"""
        
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob('visual_metadata/meme_visual_analysis.json')
            blob.upload_from_string(json.dumps(metadata_list, indent=2), content_type='application/json')
            
            print(f"Visual metadata uploaded to gs://{self.bucket_name}/visual_metadata/")
            return True
        except Exception as e:
            print(f"Visual metadata upload error: {str(e)}")
            return False
    
    def create_bucket_if_not_exists(self):
        """Create storage bucket if it doesn't exist"""
        
        try:
            bucket = self.client.get_bucket(self.bucket_name)
            print(f"Bucket {self.bucket_name} already exists")
        except:
            bucket = self.client.create_bucket(self.bucket_name, location="US")
            print(f"Bucket {self.bucket_name} created")
        
        return bucket

if __name__ == "__main__":
    manager = StorageManager()
    manager.create_bucket_if_not_exists()
