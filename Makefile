# Makefile to lint the schema, validate config.yaml files, and generate documentation

# Define variables for the schema file and config directory
SCHEMA_FILE = schema/validate_schema.yaml
DOCS_DIR = docs/developer
DOCS_OUTPUT = $(DOCS_DIR)/schema_docs.md

# 1. Generate documentation
.PHONY: gendoc
gendoc:
	@echo "Generating documentation..."
	# Create the docs directory if it doesn't exist and generate markdown documentation
	mkdir -p $(DOCS_DIR)
	touch $(DOCS_DIR)/.nojekyll  # Ensure GitHub Pages doesn’t use Jekyll
	linkml generate doc --format markdown --directory $(DOCS_DIR) $(SCHEMA_FILE)
	([ ! -f $(DOCS_DIR)/about.md ] && cp src/docs/about.md $(DOCS_DIR)/) || true
	@echo "Documentation generated at $(DOCS_OUTPUT)."

# Combined target to run generate docs and in future whatever things come at Makefile level
.PHONY: all
all: gendoc
	@echo "Developer's documentation generation completed."
