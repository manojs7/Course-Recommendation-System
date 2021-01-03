import csv
def csv_writer(course,price,rating,hours,lectures,level,search_entry):
    with open('E:/Course_Recommender/'+ search_entry +'.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name","Price","Rating","Length(in hrs)","No. of Lectures","Level"])
            print(course,price,rating,hours,lectures,level)
            #entering the enteries of the page
            for i in range(len(rating)):
                writer.writerow([course[i],price[i],rating[i],hours[i],lectures[i],level[i]])