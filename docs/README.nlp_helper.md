# extract names

    cd ${HOME}/orgs/robert.net/git/github.com/genesisinc/bible-text
    ❯ brew install uv

    ❯ uv init
        Initialized project `bible-text`

    ❯ uv add spacy
        Using CPython 3.12.6 interpreter at: /opt/homebrew/opt/python@3.12/bin/python3.12
        Creating virtual environment at: .venv
        Resolved 43 packages in 899ms
        Prepared 41 packages in 3.51s
        Installed 41 packages in 106ms
        + annotated-types==0.7.0
        + ...

    ❯ uv run python -m spacy download en_core_web_sm
        Collecting en-core-web-sm==3.8.0
        Downloading https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl (12.8 MB)
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.8/12.8 MB 20.0 MB/s eta 0:00:00
        Installing collected packages: en-core-web-sm
        Successfully installed en-core-web-sm-3.8.0
        ✔ Download and installation successful
        You can now load the package via spacy.load('en_core_web_sm')

    ❯ uv run nlp_helper.py
        Extraction complete! Check 'person-names.list' and 'place-names.list' for results.

    ❯ wc -l tmp/person-names.list tmp/place-names.list
        683 tmp/person-names.list
        397 tmp/place-names.list
        1080 total
