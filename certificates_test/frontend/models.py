from django.db import models

class TestResult(models.Model):
    common_name = models.CharField(max_length=100)
    filename_crt = models.CharField(max_length=100)
    filename_incrt = models.CharField(max_length=100)
    filename_key = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tested_at = models.DateTimeField(auto_now_add=True)
    is_test_result = models.BooleanField()
