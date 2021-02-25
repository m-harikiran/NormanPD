import argparse

import project0

def main(url):
    # Download data
    incident_data = project0.fetchincidents(url)

    # Extract data
    incidents = project0.extractincidents(incident_data)
	
    # Create new database and create table
    dbName = project0.createdb()
	
    # Insert data into incidents table
    project0.populatedb(dbName, incidents)
	
    # Print incident counts grouped by nature of incident
    project0.status(dbName)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)