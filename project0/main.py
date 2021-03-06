import argparse
import validators

import project0


def main(url):
    # Download data
    incident_data = project0.fetchIncidents(url)

    # Extract data
    incidents = project0.extractIncidents(incident_data)

    # Create new database and create table
    dbName = project0.createDB()

    # Insert data into incidents table
    project0.populateDB(dbName, incidents)

    # Print incident counts grouped by nature of incident
    project0.status(dbName)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # Creating an argument parser object
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary url.")  # Adding optinal argument --incidents

    # Parsing the arguments to check if the condition if conditions is not met this will throw an error
    args = parser.parse_args()

    # Validating URL
    if validators.url(args.incidents):
        main(args.incidents)  # Calling the main function
    else:
        print('*****INVALID URL***** \nPlease enter correct url and run program again.')
