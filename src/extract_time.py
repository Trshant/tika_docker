# import tika
# tika.initVM()
# from tika import parser
# parsed = parser.from_file('./files/sample.eml' ) ## , xmlContent=True)
# print(parsed)


import dateparser
from datetime import datetime
import spacy
import parsedatetime as pdt
import time  # Required by parsedatetime's result format


def get_date_strings(text: str) -> list[str]:
    nlp = spacy.load(
        "en_core_web_sm"
    )  # You might need to download this: python -m spacy download en_core_web_sm
    nlp.max_length = 10000000
    doc = nlp(text)
    dates = []
    for ent in doc.ents:
        if ent.label_ == "DATE":
            dates.append(ent.text)
    return dates


def to_datetime_using_parsedatetime(
    text: str, basis_date: datetime = datetime.now()
) -> datetime:
    cal = pdt.Calendar()
    result, parse_status = cal.parse(text, sourceTime=basis_date)
    if parse_status > 0:
        future_datetime = datetime(*result[:6])
        return future_datetime


def extract_dates(text, basis_date=datetime.now()) -> list[datetime.date]:
    # using spacy to get the parts of text that are calendar related.
    dates_in_text = get_date_strings(text)
    # go through the list.
    dates = []
    for part in dates_in_text:  # Split the text into words/potential date parts
        # try using dateparser...
        date_data = dateparser.parse(
            part,
            settings={"RELATIVE_BASE": basis_date},
        )
        if date_data:
            dates.append(date_data.date())
        # in case it fails....
        else:
            # use parsedatetime to try and extract data
            dates.append(to_datetime_using_parsedatetime(part, basis_date))
    # a list of datetimes should be the result.
    return [date for date in dates if isinstance(date, datetime)]


if __name__ == "__main__":
    # Example usage:
    text1 = "The event is scheduled for 2023-10-26 and also on 11/15/2024. See you by Jan 2nd, 2025."
    dates1 = extract_dates(text1)
    print(f"Dates from text1 (dateparser): {dates1}")

    text2 = "Let's plan for 2 days from now. We also had a meeting 1 week ago."
    basis = datetime.now()
    dates2 = extract_dates(text2, basis_date=basis)
    print(f"Dates from text2 (dateparser, basis: {basis}): {dates2}")

    text3 = (
        "The report was due on March 15th, 2023. Another deadline is 3 months from now."
    )
    dates3 = extract_dates(text3, basis_date=datetime(2024, 5, 1))
    print(f"Dates from text3 (dateparser, basis: 2024-05-01): {dates3}")

    text4 = "Meet me next Tuesday at 3 PM."
    dates4 = extract_dates(text4, basis_date=datetime.now())
    print(f"Dates from text4 (dateparser, basis: {datetime.now().date()}): {dates4}")

    text5 = "The deadline was last month."
    dates5 = extract_dates(text5, basis_date=datetime(2025, 4, 22))
    print(f"Dates from text5 (dateparser, basis: 2025-04-22): {dates5}")
