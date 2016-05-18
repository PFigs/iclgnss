# ics parser
# built by Pedro Silva for ICL-GNSS
# MIT license

import datetime
import icalendar as ical
UTC_OFFSET = 2

def bootstrapBoiler(content,fp):
    """creates bootstrap boilerplate with panel sections"""
    header = ("<!doctype html>"
    "<html class=\"no-js\" lang="">"
        "<head>"
            "<meta charset=\"utf-8\">"
            "<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge,chrome=1\">"
            "<title></title>"
            "<meta name=\"description\" content=\"\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            "<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css\" "
            "integrity=\"sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7\" crossorigin=\"anonymous\">"
        "</head>"
        "<body>")

    footer = ( "<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js\" integrity=\"sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS\" crossorigin=\"anonymous\"></script>"
                "</body>"
            "</html>")

    fp.write(header)
    for each in content:
        fp.write(each.encode('utf-8'))
    fp.write(footer)


def boxpost(heading,date,time,description):
    """creates theme boxpost element"""
    btag = "<section class=\"box post\">"
    etag = "</section>"
    header = addHeader(heading, date, time)
    para = "<p>" + addLineBreak(addBold(description)) + "</p>"
    return addElement(btag, header + para, etag)


def bsPanel(heading, hour, date, body):
    """creates a bootstrap panel"""
    btag = "<div class=\"panel panel-default\">"
    etag = "</div>"
    head = addHeading(heading, date, hour)
    body = addBody(addLineBreak(addBold(body)))
    return addElement(btag, head + body, etag)


#### HELPERS

def addHeading(heading, hour, date):
    btag = "<div class=\"panel-heading\"><b>"
    etag = "</b></div>"
    meta = addMeta(date, hour)
    return addElement(btag, heading + meta, etag)


def addBody(body):
    btag = "<div class=\"panel-body\">"
    etag = "</div>"
    return addElement(btag, body, etag)


def addElement(btag, val, etag):
    elem = btag + val + etag
    return elem


def addMeta(date, time):
    btag = "<ul class=\"meta\">"
    etag = "</ul>"
    body = addDate(date) + addTime(time)
    return addElement(btag, body, etag)


def addHeader(heading, date, time):
    btag = "<header>"
    etag = "</header>"
    body = "<p><b>" + heading + "</b></p>"
    meta = addMeta(date, time)
    return addElement(btag, body + meta, etag)


def addBold(text):
    lines = list(text.split("\n"))
    for i, s in enumerate(lines):
        if 'Abstract' in s:
            lines[i] = '<b>' + s + '</b>'

        if 'Biography' in s:
            lines[i] = '<b>' + s + '</b>'

        if 'papers' in s:
            del(lines[i])
        if ':' in s:
            if s.count(':') == 1:
                lines[i] = '<b>' + s + '</b>'

    return "\n".join(lines)


def addDate(date):
    btag = "<li class=\"icon fa-calendar\">"
    etag = "</li>"
    return addElement(btag, date, etag)


def addTime(time):
    btag = "<li class=\"icon fa-clock-o\">"
    etag = "</li>"
    return addElement(btag, time, etag)


def addLineBreak(text):
    return "<br/>".join(text.split("\n"))

if __name__ == "__main__":
    fin = open('iclgnss.ics', 'rb')
    cal = ical.Calendar.from_ical(fin.read())
    bootstrap = list()
    txt = list()

    # ical in UTC time
    dutc = datetime.timedelta(hours=UTC_OFFSET)

    # create element for each event
    for event in cal.walk('vevent'):
        if 'Session' in event['SUMMARY']:
            cet = event['DTSTART'].dt + dutc
            sHour = cet.strftime("%H:%M")
            sDate = cet.strftime("%d.%m")
            # following bootstrap
            bootstrap.append(
                bsPanel(
                    event['SUMMARY'],
                    sHour,
                    sDate,
                    event['DESCRIPTION'])
            )

            # following website theme
            txt.append(
                boxpost(event['SUMMARY'],
                sDate,
                sHour,
                event['DESCRIPTION'])
            )

    # full index.html
    fout = open('index.html', 'w')
    bootstrapBoiler(bootstrap, fout)

    fout = open('bootstrap.html', 'w')
    for each in bootstrap:
        fout.write(each.encode('utf-8'))

    fout = open('txt.html', 'w')
    for each in txt:
        fout.write(each.encode('utf-8'))
