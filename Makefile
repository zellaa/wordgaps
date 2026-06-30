.PHONY: find-words plot

find-words:
	uv run main.py

# Trick to allow passing a word directly as an argument, e.g., "make plot bar"
ifeq (plot,$(firstword $(MAKECMDGOALS)))
  # Use the rest of the command line arguments as the word
  PLOT_WORD := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # Turn the arguments into do-nothing targets so make doesn't complain about unknown targets
  $(eval $(PLOT_WORD):;@:)
endif

plot:
	@if [ -z "$(PLOT_WORD)" ]; then \
		echo "Error: Please specify a word, e.g., 'make plot bar'"; \
		exit 1; \
	fi
	uv run plotter.py $(PLOT_WORD)
	open wordgap.png
