.PHONY: generate validate check derive coverage all clean

all: generate validate

generate:
	@python3 scripts/theme.py generate

validate:
	@python3 scripts/theme.py validate

check:
	@python3 scripts/theme.py check

derive:
	@python3 scripts/theme.py derive

coverage:
	@python3 scripts/theme.py coverage

clean:
	@rm -f themes/synthwave84.json

help:
	@echo "Usage:"
	@echo "  make generate  - Build theme from src/base.json + palette.json"
	@echo "  make validate  - Check theme structure and accessibility"
	@echo "  make check     - Verify theme matches source files"
	@echo "  make derive    - Show programmatically derived variant colors"
	@echo "  make coverage  - Check Zed token coverage"
	@echo "  make all       - Generate and validate"
