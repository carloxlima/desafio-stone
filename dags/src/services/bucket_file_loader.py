import requests
from bs4 import BeautifulSoup


class BucketFileLoader:
    """
    Class to load files from a Google Cloud Storage bucket.
    This class is used to get the link of all files in the bucket.
    
    """
    url_files = []

    def __init__(self, link_bucket):
        self.link = link_bucket
    
    def get_file_link(self):
        """
        Get the link of all files in the bucket.
        The link is a list of URLs to the files in the bucket.
        The files are in parquet and jpg format.

        """
        response = requests.get(self.link)
        if response.status_code == 200:
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            values =  soup.find_all('key')
            url_files = [f'{self.link}{val.text}' for val in values]
            self.url_files = url_files

        else:
            raise Exception(f"Failed to get files from bucket: {response.status_code}")
    
    def get_files_parquet(self):
        """
        Get the link of all parquet files in the bucket.
        """
        return [val for val in self.url_files if val.endswith('.pq')]
    
    def get_files_img(self):
        """
        Get the link of all image files in the bucket.  
        """ 
        return [val for val in self.url_files if val.endswith('.jpg')]