from rest_framework import serializers


class TokenRequestSerializer(serializers.Serializer):
	email = serializers.CharField(required=True, allow_blank=False, max_length=254)
	password = serializers.CharField(required=True, allow_blank=False, max_length=254)
	claims = serializers.DictField(required=False, child=serializers.CharField())

	def update(self, instance, validated_data):
		pass

	def create(self, validated_data):
		pass


class VerificationRequestSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True, allow_blank=False, max_length=254)
	validation_key = serializers.IntegerField(required=True)

	def update(self, instance, validated_data):
		pass

	def create(self, validated_data):
		pass


class ProspectRequestSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True, allow_blank=False, max_length=254)

	def update(self, instance, validated_data):
		pass

	def create(self, validated_data):
		pass
