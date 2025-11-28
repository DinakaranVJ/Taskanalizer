from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField()
    due_date = serializers.DateField(required=False)
    estimated_hours = serializers.FloatField()
    importance = serializers.IntegerField()
    dependencies = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

    def validate_importance(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Importance must be 1-10")
        return value

    def validate_estimated_hours(self, value):
        if value <= 0:
            raise serializers.ValidationError("Estimated hours must be positive")
        return value
