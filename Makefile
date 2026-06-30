.PHONY: find-words plot generate-valid-words

find-words:
	uv run wordgaps --find-longest

generate-valid-words:
	uv run wordgaps --generate-valid

ifeq (plot,$(firstword $(MAKECMDGOALS)))
  PLOT_WORD := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(PLOT_WORD):;@:)
endif

plot:
	@if [ -z "$(PLOT_WORD)" ]; then \
		echo "Error: Please specify a word, e.g., 'make plot bar'"; \
		exit 1; \
	fi
	uv run wordgaps --plot $(PLOT_WORD)
	open output-images/$(shell echo $(PLOT_WORD) | tr A-Z a-z).png
