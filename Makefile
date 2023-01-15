.PHONY: tests

tests:
	@poetry run pytest --doctest-modules --junitxml=test-results.xml --cov=crudhex --cov-report=html

generate/types_file:
	@poetry run python scripts/jdk_classes_export.py

# Update version, commit and tag
# RULE: Rule to generate the version (patch, minor, major)
version-update:
	@bin/version-update.sh $(RULE)