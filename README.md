# bible text - analysis & data science

A hobby project to extract entities like Person, Date, ORG, NPE, Occupations, NORP etc mentioned in the bible.
Looking to extend it to usable in some bible based analysis & data science tasks, which can
help in developing talks, writing articles to help readers learn from Bible's wisdom.

Need help to test, suggest new features, involved in development and etc.
Like to be a part?

Note

- Data and reports you see here are UNVERIFIED
- Expected accuracy is about 50-60%
- Most of the reports are based on NWT 2013-English bible

## usage - sample reports

- legends

        ❯ task legends
            +------------+-------+----------------------------------------------+
            | Type       | count | Explanation                                  |
            +------------+-------+----------------------------------------------+
            | PERSON     | 17662 | Names of individuals                         |
            | DATE       | 3432  | Explicit or implicit date expressions        |
            | GPE        | 9478  | Geopolitical entities (places)               |
            | ORG        | 4254  | Organizations or groups                      |
            | OCCUPATION | 6273  | Roles or professions                         |
            | NORP       | 1380  | Nationalities, religious or political groups |
            +------------+-------+----------------------------------------------+

- names recorded in the bible

        ❯ task names
            Summary:
            Total: 17662 records
            Showing 16 of 17662 records
            +----+------------+---------+-------+--------+---------+
            | n  | Book       | Chapter | Verse | Type   | Text    |
            +----+------------+---------+-------+--------+---------+
            | 1  | genesis    | 1       | 3     | PERSON | God     |
            | 2  | genesis    | 2       | 4     | PERSON | Jehovah |
            | 3  | genesis    | 2       | 5     | PERSON | bush    |
            | 4  | genesis    | 2       | 5     | PERSON | Jehovah |
            | 5  | genesis    | 2       | 7     | PERSON | Jehovah |
            | 6  | genesis    | 2       | 8     | PERSON | Jehovah |
            | 7  | genesis    | 2       | 11    | PERSON | Havilah |
            | 8  | genesis    | 2       | 13    | PERSON | Gihon   |
            | 9  | revelation | 22      | 5     | PERSON | Jehovah |
            | 10 | revelation | 22      | 6     | PERSON | Jehovah |
            | 11 | revelation | 22      | 8     | PERSON | John    |
            | 12 | revelation | 22      | 13    | PERSON | Alpha   |
            | 13 | revelation | 22      | 16    | PERSON | Jesus   |
            | 14 | revelation | 22      | 16    | PERSON | David   |
            | 15 | revelation | 22      | 20    | PERSON | Jesus   |
            | 16 | revelation | 22      | 21    | PERSON | Jesus   |
            +----+------------+---------+-------+--------+---------+

- distinct names

        ❯ task unique-names
            Summary:
            Total: 1656 records
            Showing 16 of 1656 records
            +----+-----------------------+-------+
            | n  | Text                  | count |
            +----+-----------------------+-------+
            | 1  | Aaron                 | 308   |
            | 2  | Abarim                | 2     |
            | 3  | Abdi                  | 2     |
            | 4  | Abdiel                | 1     |
            | 5  | Abdon                 | 5     |
            | 6  | Abdon the son         | 1     |
            | 7  | Abednego              | 13    |
            | 8  | Abel                  | 18    |
            | 9  | mosaic pebbles        | 1     |
            | 10 | myrrh                 | 6     |
            | 11 | myrrh Spending        | 1     |
            | 12 | pervert righteousness | 1     |
            | 13 | the Creator           | 1     |
            | 14 | the King of           | 1     |
            | 15 | the King of Israel    | 2     |
            | 16 | the King of Jacob     | 1     |
            +----+-----------------------+-------+

- most frequent names

        ❯ task top-names
            Summary:
            Total: 10 records
            Showing all 10 records
            +----+---------+-------+
            | n  | Text    | count |
            +----+---------+-------+
            | 1  | Joshua  | 217   |
            | 2  | Abraham | 227   |
            | 3  | Joseph  | 227   |
            | 4  | Solomon | 255   |
            | 5  | Jacob   | 269   |
            | 6  | Aaron   | 308   |
            | 7  | Saul    | 326   |
            | 8  | Jesus   | 793   |
            | 9  | David   | 904   |
            | 10 | Jehovah | 5161  |
            +----+---------+-------+

- Organizations mentioned

        ❯ task org
            Summary:
            Total: 4254 records
            Showing 16 of 4254 records
            +----+------------+---------+-------+------+----------+
            | n  | Book       | Chapter | Verse | Type | Text     |
            +----+------------+---------+-------+------+----------+
            | 1  | genesis    | 2       | 11    | ORG  | Pishon   |
            | 2  | genesis    | 4       | 1     | ORG  | Cain     |
            | 3  | genesis    | 4       | 2     | ORG  | Cain     |
            | 4  | genesis    | 4       | 3     | ORG  | Cain     |
            | 5  | genesis    | 4       | 5     | ORG  | Cain     |
            | 6  | genesis    | 4       | 5     | ORG  | Cain     |
            | 7  | genesis    | 4       | 8     | ORG  | Cain     |
            | 8  | genesis    | 4       | 8     | ORG  | Cain     |
            | 9  | revelation | 9       | 11    | ORG  | Apollyon |
            | 10 | revelation | 11      | 8     | ORG  | Sodom    |
            | 11 | revelation | 12      | 9     | ORG  | Devil    |
            | 12 | revelation | 12      | 12    | ORG  | Devil    |
            | 13 | revelation | 19      | 7     | ORG  | Lamb     |
            | 14 | revelation | 20      | 2     | ORG  | Devil    |
            | 15 | revelation | 21      | 6     | ORG  | Omega    |
            | 16 | revelation | 22      | 13    | ORG  | Omega    |
            +----+------------+---------+-------+------+----------+
            Legend.ORG - Organization or groups

- Organizations summary

        ❯ task occupation-summary
            top and bottom 8 of sorted by occupation
                Summary:
                Total: 44 records
                Showing 16 of 44 records
                +----+-------------+-------+
                | n  | occupation  | count |
                +----+-------------+-------+
                | 1  | astrologer  | 8     |
                | 2  | baker       | 11    |
                | 3  | beggar      | 5     |
                | 4  | carpenter   | 2     |
                | 5  | charioteer  | 8     |
                | 6  | cook        | 12    |
                | 7  | cupbearer   | 13    |
                | 8  | elder       | 188   |
                | 9  | slave       | 309   |
                | 10 | soldier     | 76    |
                | 11 | spy         | 42    |
                | 12 | stonecutter | 8     |
                | 13 | teacher     | 64    |
                | 14 | tentmaker   | 1     |
                | 15 | trader      | 9     |
                | 16 | weaver      | 4     |
                +----+-------------+-------+

            top and bottom 8 of sorted by count
                Summary:
                Total: 44 records
                Showing 16 of 44 records
                +----+-------------+-------+
                | n  | occupation  | count |
                +----+-------------+-------+
                | 1  | perfumer    | 1     |
                | 2  | executioner | 1     |
                | 3  | tentmaker   | 1     |
                | 4  | mason       | 2     |
                | 5  | fisher      | 2     |
                | 6  | carpenter   | 2     |
                | 7  | goldsmith   | 3     |
                | 8  | weaver      | 4     |
                | 9  | shepherd    | 129   |
                | 10 | elder       | 188   |
                | 11 | judge       | 287   |
                | 12 | slave       | 309   |
                | 13 | prophet     | 459   |
                | 14 | servant     | 828   |
                | 15 | priest      | 957   |
                | 16 | king        | 2448  |
                +----+-------------+-------+

- Occupations

        ❯ task occupation
            task: [occupation] mlr --csv --from data/bible_entities.csv filter '$Type == "OCCUPATION"'  > tmp/out.csv

            Summary:
            Total: 6273 records
            Showing 16 of 6273 records
            +----+------------+---------+-------+------------+----------+
            | n  | Book       | Chapter | Verse | Type       | Text     |
            +----+------------+---------+-------+------------+----------+
            | 1  | genesis    | 4       | 2     | OCCUPATION | shepherd |
            | 2  | genesis    | 9       | 20    | OCCUPATION | farmer   |
            | 3  | genesis    | 9       | 25    | OCCUPATION | slave    |
            | 4  | genesis    | 9       | 26    | OCCUPATION | slave    |
            | 5  | genesis    | 9       | 27    | OCCUPATION | slave    |
            | 6  | genesis    | 10      | 9     | OCCUPATION | hunter   |
            | 7  | genesis    | 10      | 9     | OCCUPATION | hunter   |
            | 8  | genesis    | 12      | 16    | OCCUPATION | servant  |
            | 9  | revelation | 20      | 13    | OCCUPATION | judge    |
            | 10 | revelation | 21      | 24    | OCCUPATION | king     |
            | 11 | revelation | 22      | 3     | OCCUPATION | slave    |
            | 12 | revelation | 22      | 5     | OCCUPATION | king     |
            | 13 | revelation | 22      | 6     | OCCUPATION | prophet  |
            | 14 | revelation | 22      | 6     | OCCUPATION | slave    |
            | 15 | revelation | 22      | 9     | OCCUPATION | slave    |
            | 16 | revelation | 22      | 9     | OCCUPATION | prophet  |
            +----+------------+---------+-------+------------+----------+

- most frequently mentioned occupations

        ❯ task top-occupations
        Summary:
        Total: 10 records
        Showing all 10 records
        +----+----------+-------+
        | n  | Text     | count |
        +----+----------+-------+
        | 1  | soldier  | 76    |
        | 2  | governor | 76    |
        | 3  | shepherd | 129   |
        | 4  | elder    | 188   |
        | 5  | judge    | 287   |
        | 6  | slave    | 309   |
        | 7  | prophet  | 459   |
        | 8  | servant  | 828   |
        | 9  | priest   | 957   |
        | 10 | king     | 2448  |
        +----+----------+-------+

- distinct occupations

        ❯ task unique-occupation
        Summary:
        Total: 44 records
        Showing 16 of 44 records
        +----+-------------+-------+
        | n  | Text        | count |
        +----+-------------+-------+
        | 1  | astrologer  | 8     |
        | 2  | baker       | 11    |
        | 3  | beggar      | 5     |
        | 4  | carpenter   | 2     |
        | 5  | charioteer  | 8     |
        | 6  | cook        | 12    |
        | 7  | cupbearer   | 13    |
        | 8  | elder       | 188   |
        | 9  | slave       | 309   |
        | 10 | soldier     | 76    |
        | 11 | spy         | 42    |
        | 12 | stonecutter | 8     |
        | 13 | teacher     | 64    |
        | 14 | tentmaker   | 1     |
        | 15 | trader      | 9     |
        | 16 | weaver      | 4     |
        +----+-------------+-------+

- Geo Political Entities(gpe)

        ❯ task gpe
            Summary:
            Total: 9478 records
            Showing 16 of 9478 records
            +----+------------+---------+-------+------+----------------+
            | n  | Book       | Chapter | Verse | Type | Text           |
            +----+------------+---------+-------+------+----------------+
            | 1  | genesis    | 2       | 8     | GPE  | Eden           |
            | 2  | genesis    | 2       | 10    | GPE  | Eden           |
            | 3  | genesis    | 2       | 14    | GPE  | Assyria        |
            | 4  | genesis    | 2       | 15    | GPE  | Eden           |
            | 5  | genesis    | 3       | 23    | GPE  | Eden           |
            | 6  | genesis    | 3       | 24    | GPE  | Eden           |
            | 7  | genesis    | 4       | 1     | GPE  | Jehovah        |
            | 8  | genesis    | 4       | 16    | GPE  | Eden           |
            | 9  | revelation | 7       | 4     | GPE  | Israel         |
            | 10 | revelation | 7       | 6     | GPE  | Naphtali       |
            | 11 | revelation | 11      | 8     | GPE  | Egypt          |
            | 12 | revelation | 11      | 15    | GPE  | the Kingdom of |
            | 13 | revelation | 12      | 10    | GPE  | the Kingdom of |
            | 14 | revelation | 21      | 2     | GPE  | New Jerusalem  |
            | 15 | revelation | 21      | 10    | GPE  | Jerusalem      |
            | 16 | revelation | 21      | 12    | GPE  | Israel         |
            +----+------------+---------+-------+------+----------------+
            Legend.GPE - GeoPoliticalEntity

- dates mentioned

        ❯ task date
            task: [date] mlr --c2p --barred --from bible_entities.csv \
            filter '$Type == "DATE" && $Book == "daniel"' \
                then head

            +--------+---------+-------+------+---------------------+
            | Book   | Chapter | Verse | Type | Text                |
            +--------+---------+-------+------+---------------------+
            | daniel | 1       | 1     | DATE | the third year      |
            | daniel | 1       | 5     | DATE | daily               |
            | daniel | 1       | 5     | DATE | three years         |
            | daniel | 1       | 7     | DATE | Shadrach            |
            | daniel | 1       | 12    | DATE | ten days            |
            | daniel | 1       | 14    | DATE | ten days            |
            | daniel | 1       | 15    | DATE | the end of ten days |
            | daniel | 1       | 21    | DATE | the first year      |
            | daniel | 2       | 1     | DATE | the second year     |
            | daniel | 2       | 28    | DATE | the days            |
            +--------+---------+-------+------+---------------------+

- date-summary

        ❯ task date-summary
            Summary:
            Total: 10 records
            Showing all 10 records
            +----+-----------------+-------+
            | n  | Text            | count |
            +----+-----------------+-------+
            | 1  | the light Day   | 1     |
            | 2  | a first day     | 1     |
            | 3  | a third day     | 1     |
            | 4  | between the day | 1     |
            | 5  | days            | 26    |
            | 6  | years           | 25    |
            | 7  | the day         | 312   |
            | 8  | day             | 9     |
            | 9  | a fourth day    | 1     |
            | 10 | a fifth day     | 1     |
            +----+-----------------+-------+

- Nationalities Religions or Political Groups (norp)

        ❯ task norp
            Summary:
            Total: 1380 records
            Showing 16 of 1380 records
            +----+------------+---------+-------+------+-----------+
            | n  | Book       | Chapter | Verse | Type | Text      |
            +----+------------+---------+-------+------+-----------+
            | 1  | genesis    | 6       | 5     | NORP | mans      |
            | 2  | genesis    | 8       | 21    | NORP | mans      |
            | 3  | genesis    | 10      | 4     | NORP | Tarshish  |
            | 4  | genesis    | 10      | 18    | NORP | Zemarite  |
            | 5  | genesis    | 11      | 18    | NORP | Reu       |
            | 6  | genesis    | 11      | 28    | NORP | Chaldeans |
            | 7  | genesis    | 11      | 31    | NORP | Chaldeans |
            | 8  | genesis    | 12      | 12    | NORP | Egyptians |
            | 9  | revelation | 17      | 14    | NORP | Lamb      |
            | 10 | revelation | 18      | 13    | NORP | Indian    |
            | 11 | revelation | 21      | 14    | NORP | Lamb      |
            | 12 | revelation | 21      | 17    | NORP | mans      |
            | 13 | revelation | 21      | 22    | NORP | Lamb      |
            | 14 | revelation | 21      | 23    | NORP | Lamb      |
            | 15 | revelation | 22      | 1     | NORP | Lamb      |
            | 16 | revelation | 22      | 3     | NORP | Lamb      |
            +----+------------+---------+-------+------+-----------+
            Legend.NORP - Nationalities Religions or Political Groups

- search for words, numbers or phrases

        1❯ task search -- jonathan
            Showing top 5 of 105 matches
            +--------------+---------+-------+----------------------------------------------------------------------+
            | book         | chapter | verse | text                                                                 |
            +--------------+---------+-------+----------------------------------------------------------------------+
            | nehemiah     | 12      | 14    | for Malluchi, Jonathan; for Shebaniah, Joseph;                       |
            | 2 samuel     | 23      | 32    | Eliahba the Shaalbonite, the sons of Jashen, Jonathan,               |
            | 2 samuel     | 1       | 17    | Then David chanted this dirge over Saul and his son Jonathan         |
            | 1 samuel     | 20      | 4     | Then Jonathan said to David: Whatever you say, I will do for you.    |
            | 1 chronicles | 8       | 34    | And Jonathans son was Merib baal. Merib baal became father to Micah. |
            +--------------+---------+-------+----------------------------------------------------------------------+

        2❯ task search -- "declares the Sovereign Lord Jehovah"
            Showing top 5 of 87 matches
            +---------+---------+-------+---------------------------------------------------------------------------------------------------------+
            | book    | chapter | verse | text                                                                                                    |
            +---------+---------+-------+---------------------------------------------------------------------------------------------------------+
            | ezekiel | 16      | 23    | After all your evil, woe, woe to you, declares the Sovereign Lord Jehovah.                              |
            | amos    | 3       | 13    | Hear and warn the house of Jacob, declares the Sovereign Lord Jehovah, the God of armies.               |
            | ezekiel | 39      | 5     | You will fall on the open field, for I myself have spoken, declares the Sovereign Lord Jehovah.         |
            | ezekiel | 11      | 8     | A sword you have feared, and a sword I will bring against you, declares the Sovereign Lord Jehovah.     |
            | ezekiel | 34      | 15    | I myself will feed my sheep, and I myself will make them lie down, declares the Sovereign Lord Jehovah. |
            +---------+---------+-------+---------------------------------------------------------------------------------------------------------+

        3❯ task search -- 930
            Showing top 2 of 2 matches
            +----------+---------+-------+------------------------------------------------------------------------+
            | book     | chapter | verse | text                                                                   |
            +----------+---------+-------+------------------------------------------------------------------------+
            | nehemiah | 7       | 38    | the sons of Senaah, 3,930.                                             |
            | genesis  | 5       | 5     | So all the days of Adams life amounted to 930 years, and then he died. |
            +----------+---------+-------+------------------------------------------------------------------------+

        4❯ task search -- "Jehovah of armies"
            Showing top 5 of 249 matches
            +-----------+---------+-------+------------------------------------------------------------------+
            | book      | chapter | verse | text                                                             |
            +-----------+---------+-------+------------------------------------------------------------------+
            | zechariah | 8       | 1     | The word of Jehovah of armies again came, saying:                |
            | zechariah | 7       | 4     | The word of Jehovah of armies again came to me, saying:          |
            | zechariah | 8       | 18    | The word of Jehovah of armies again came to me, saying:          |
            | psalms    | 84      | 12    | O Jehovah of armies, Happy is the man who trusts in you.         |
            | isaiah    | 39      | 5     | Isaiah now said to Hezekiah: Hear the word of Jehovah of armies, |
            +-----------+---------+-------+------------------------------------------------------------------+

- get bible text using references

        ❯ task ref -- genesis 1:1
            In the beginning God created the heavens and the earth.

        ❯ task ref -- genesis 1:1-1:6
            In the beginning God created the ... the waters.

        ❯ task ref -- genesis 1:25-2:2
            And God went on to make the wild animals of the ... been doing.

        ❯ task ref -- song of solomon 1:3
            The fragrance of your oils is pleasant. Your name is like a fragrant oil poured out. That is why the young women love you.

        ❯ task ref -- 2 john 2
            because of the truth that remains in us and will be with us forever.

        ❯ task ref -- 2 john 1:2
            because of the truth that remains in us and will be with us forever.

## requirements

- [go-task/task](https://github.com/go-task/task)
- [astral-sh/uv](https://github.com/astral-sh/uv)
- [miller](https://github.com/johnkerl/miller)
- [jqlang/jq](https://github.com/jqlang/jq) (optional)
- [py-nlp-spacy-uv](./README.nlp_helper.md)

## one-time tasks

If you have the bible text in files, we need to load them to a json file using below task.

- generate bible-data.json from files

        ❯ task generate-json
            task: [generate-json] uv run bible.py --generate

        Bible data successfully written to bible_data.json

Now, you have the whole bible in a single file: bible_data.json instead of ~1200 files.

Once we have the bible_data.json from above task, we can parse and extract the interested details using below task.

- extract entities

        ❯ task extract
            task: [extract] uv run bible.py \
            --extract \
            --bible-json "bible_data.json" \
            --output-json "bible_entities.json" \
            --output-csv "bible_entities.csv"

        Entity and occupation extraction complete. JSON results saved to bible_entities.json
        CSV results saved to bible_entities.csv

Now, you have bible_entities.json bible_entities.csv with below summary of entities.

You may proceed to use other tasks to query occupations, persons, orgs etc mentioned in bible.
Please remember these data is generated programmatically and accuracy is about 50%
