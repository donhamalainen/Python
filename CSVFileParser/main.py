import os

# Open and read the CSV file
def read_csv(filename):
    unique_projects = set() 
    unique_rows = []

    if os.path.exists(filename):
        with open(filename, "r") as file:
            header = file.readline().strip()
            unique_rows.append(header)

            # Read each line in the CSV file
            for line in file:
                values = line.strip().split(",")
                project_name = values[1] 
                
                # Cheking
                if project_name not in unique_projects:
                    unique_projects.add(project_name)
                    # Generate GitHub link for the project
                    github_link = generate_github_links(project_name)
                    values.append(github_link)
                    unique_rows.append(",".join(values))
                
        # Writing  
        with open(filename, "w") as output_file:
            for row in unique_rows:
                output_file.write(row + "\n")

        return unique_projects
    else:
        print(f"File {filename} not found.")


# We now that the links start https://github.com/apache/{something}
def generate_github_links(project_name):
     # Remove 'apache' prefix and any leading '-' or '_'
    if project_name.startswith('apache'):
        project_name = project_name[6:]
        if project_name.startswith('-') or project_name.startswith('_'):
            project_name = project_name[1:] 
    github_link = f"https://github.com/apache/{project_name}"
    return github_link


# Defining main function
def main():
    read_csv("sonar_measures.csv")

# Using the special variable 
if __name__=="__main__":
    main()
