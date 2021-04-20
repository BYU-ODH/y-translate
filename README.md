# Adding new SupportedLanguage

To add support for a new language, follow these steps.

First, verify that the language is supported by StanfordNLP at https://stanfordnlp.github.io/stanfordnlp/models.html.

Second, download the language model. Open a Python repl and run the following code:

```
>>> import stanfordnlp
>>> stanfordnlp.download('en')
```

Third, add the language code to the SupportedLanguage class.