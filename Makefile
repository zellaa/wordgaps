.PHONY: find-words plot

find-words:
	uv run main.py

ifeq (plot,$(firstword $(MAKECMDGOALS)))
  PLOT_WORD := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(PLOT_WORD):;@:)
endif

plot:
	@if [ -z "$(PLOT_WORD)" ]; then \
		echo "Error: Please specify a word, e.g., 'make plot bar'"; \
		exit 1; \
	fi
	uv run plotter.py $(PLOT_WORD)
	open wordgap.png
