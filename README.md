# akinator-gpt

## Getting Started
Install using `environment.yml` file. This can be done by running

```
conda env create -f environment.yml
```

All API keys are managed in `keys.py` as string variables. The only used variable is `OPENAI_API`. Please **do not change the name of these variables**. This will not work otherwise (*for now*). 

To run, simply run `aki.py`. This will save conversations with Akinator in `logs/` with appended answer and guess rows at the end.

### Supported Models

- `user`: Play with Akinator directly using your terminal!
- `gpt`: Run gpt-3.5-turbo. Of course, this supports more recent models as well since it uses the API. However, we have not seen a large performance boost that warrants the added cost.

### Future Plans

- Add environment variable support for API keys
- Planning to add support for additional models: `Llama3`, `Mistral`
- Automatic analysis for generated runs

### Credits

This project heavily utilizes the `akipy` package, a very cool Python wrapper for the Akinator website. 

Please support that project [here](https://github.com/advnpzn/akipy/)!

### Bugs and Fixes

- Implment history tracking for `User` model