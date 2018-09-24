# Purpose

Various analyses in the energy domain rely on unique and hard-to-access data. In particular, it can be very difficult to find and parse utility data, even that which is publicly and openly available on the Web. This is largely a result of the ever-changing nature of holding companies, mergers, acquisitions, etc. causing Web domains for these entities to be extremely dynamic, making even annual updates of existing data source labor-intensive.

This project aims to understand the viability of a Web crawler + scraping system that can keep up with this fluid industry by taking a bite out of a relatively well-defined problem: cataloging the rates that are used for billing customers of U.S. electric utilities.

# The Data

No data obtained by this work shall be outside the public domain. If it is readily accessible without any special credentials (including usernames and passwords) and not blocked by a robots.txt provision for web crawlers, then the intent is to retrieve it and catalog the file or the HTML information. 

It is expected, based upon prior experience, that a majority of the data will be contained within PDFs. As a future step, I may attempt to use OCR, PDF text conversion, and image recognition to tease out the numeric content we seek, but for now I will be satisfied with simply logging anything and everything we can find at the URLs we know were good as of 2017.

# Acknowledgements

I appreciate the aid and collaboration of the National Renewable Energy Lab team run by Debbie Brodt-Giles in working with me to understand how to improve the existing process for collecting utility rates. This team has, for years, maintained the [Utility Rates Database](https://openei.org/apps/USURDB/) and done a fantastic job with it. With their help, I'm hoping to make this job a little easier, cheaper, and faster.