import streamlit as st
import csv
import sys
import time
from itertools import islice

from util import Node, QueueFrontier
light_colors = ["#f2f2f2", "#e6f7ff", "#e6ffe6", "#fff2e6", "#ffe6f7", "#f7e6ff", "#e6fff7", "#ffe6e6", "#fff7e6", "#e6fff7"]
directory = "small"

@st.cache_data
def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    people_data = {}
    names_data = {}
    movies_data = {}

    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people_data[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names_data:
                names_data[row["name"].lower()] = {row["id"]}
            else:
                names_data[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies_data[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people_data[row["person_id"]]["movies"].add(row["movie_id"])
                movies_data[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

    return people_data, names_data, movies_data

@st.cache_data
def load_people(directory):
    return load_data(directory)[0]

@st.cache_data
def load_names(directory):
    return load_data(directory)[1]

@st.cache_data
def load_movies(directory):
    return load_data(directory)[2]

people = load_people(directory)
names = load_names(directory)
movies = load_movies(directory)

# button_check_source = st.button('Check Source')
# button_confirm_source = st.button('Confirm Source')


def main():
    st.title("Degrees of Separation App")


    # data_selection = st.selectbox(
    #     "Select a Data Source:", ["Small Data","Large Data"]
    # )
    
    data_load_status = st.empty()

    # directory = "large" if data_selection == "Large Data" else "small"
    #st.markdown(f'<p>This is a <span style="padding: 1px 4px 3px 4px; border-radius: 5px; background: #f5dcfa; font-weight: bold">paragraph</span></p>',unsafe_allow_html=True)
    data_load_status.write("Loading Data...")
    
    data_load_status.markdown(f'<span style="font-style: italic; color: green;">Data load</span>', unsafe_allow_html=True)
    
    # Print the first 5 key-value pairs
    # for key, value in islice(people.items(), 5):
    #     print(f"{key}: {value}")

    # print(f'birth : {people[11]["birth"]}')

        # inilialize state to false all
    if "button_check_source" not in st.session_state:
        st.session_state["button_check_source"] = False
    
    if "button_confirm_source" not in st.session_state:
        st.session_state["button_confirm_source"] = False

    if "button_check_target" not in st.session_state:
        st.session_state["button_check_target"] = False
    
    if "button_confirm_target" not in st.session_state:
        st.session_state["button_confirm_target"] = False

    if "button_submit_result" not in st.session_state:
        st.session_state["button_submit_result"] = False

    if "source" not in st.session_state:
        st.session_state["source"] = None
    
    if "target" not in st.session_state:
        st.session_state["target"] = None

    source_name = st.text_input("Enter the source person's name: ")

    if st.button("Check Source"):
        #print(people)
        st.session_state["button_check_source"] = not st.session_state["button_check_source"]
        
    if st.session_state["button_check_source"]:
        source = person_id_for_name(source_name)
        if source is None:
            st.error("Source Person not found.")
        elif type(source) is list:
            # print(source)
            st.warning("Source Person are having more than one!! Chose one below")
            for person in source:

                st.write(f'Person ID: {person["person_id"]}, Birth: {person["birth"]}.')

            source = st.text_input("Choose one Source perosn by ID: ")
            # Button 2 will show up
            if st.button("Confirm Source"):
                # "Button 2 is clicked" => st.session_state["button2"] = True
                st.session_state["button_confirm_source"] = not st.session_state["button_confirm_source"]
                # do some operation here
                #st.write(source)
                st.session_state["source"] = source

        else:
            # TODO: the case where it is normal
            #st.write(source)
            st.session_state["source"] = source

    # check if the source is already add to session
    if st.session_state["source"] is not None:
        source = st.session_state["source"]
        st.write(f'source person ID: {source}')
        # start adding handle target
        target_name = st.text_input("Enter the Target person's name: ")
        # st.session_state["source"] = source # prevent source from changing to None
        #st.write(f'source person ID: {source}')
        if st.button("Check Target"):
            st.session_state["button_check_target"] = not st.session_state["button_check_target"]
            # st.session_state["button_confirm_source"] = not st.session_state["button_confirm_source"]
            
        
        if st.session_state["button_check_target"] and st.session_state["source"] is not None:
            target = person_id_for_name(target_name)
            if target is None:
                st.error("Target Person not found.")
            elif type(target) is list:
                st.warning("Target Person are having more than one!! Chose one below")
                for person in target:
                    st.write(f'Person ID: {person["person_id"]}, Birth: {person["birth"]}.')

                target = st.text_input("Choose one Target perosn by ID: ")
                # Button 2 will show up
                if st.button("Confirm Target"):
                    # "Button 2 is clicked" => st.session_state["button2"] = True
                    st.session_state["button_confirm_target"] = not st.session_state["button_confirm_target"]
                    # do some operation here
                    st.session_state["target"] = target
            else:
                st.session_state["target"] = target
        
    if st.session_state["source"] is not None and st.session_state["target"] is not None:
        source = st.session_state["source"]
        target = st.session_state["target"]
        st.write(f'Source Person ID: {source}, Target Person ID: {target}')

        calculating_loading = st.empty()
        calculating_loading.write("Calculating shortest path...")

        container = st.empty()
        # Showing GIF
        container.image("Girl Cycling in autumn.gif")
        node_explore_show = st.empty()

        #convert to integer and calculate degree of saparation here

        path = shortest_path(source, target, node_explore_show)

        if path is None:
            st.error("These Two Person Are Not connected.")
        else:
            #st.markdown(f'<p>This is a <span style="padding: 1px 4px 3px 4px; border-radius: 5px; background: #f5dcfa; font-weight: bold">paragraph</span></p>',unsafe_allow_html=True)
            degrees = len(path)
            source_person_name = people[source]["name"]
            target_person_name = people[path[-1][1]]["name"]
            st.write(f'<span style="font-size: 30px; font-weight: bold; margin-right: 5px;">{degrees}</span> degrees of separation from '
                     f'<span style="padding: 1px 4px 3px 4px; border-radius: 5px; background: {light_colors[0]}; font-weight: bold">{source_person_name}</span> to'
                     f'<span style="padding: 1px 4px 3px 4px; border-radius: 5px; background: {light_colors[degrees]}; font-weight: bold">{target_person_name}</span>', unsafe_allow_html=True)
            
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                st.write(f'{i + 1}: <span style="padding: 1px 4px 3px 4px; border-radius: 5px; background: {light_colors[i]}; font-weight: bold">{person1}</span> and '
                         f'<span style="padding: 1px 4px 3px 4px; border-radius: 5px; background: {light_colors[i+1]}; font-weight: bold">{person2}</span> '
                         f'starred in <span style="font-style: italic; font-weight: bold;">{movie}<span>', unsafe_allow_html=True)
                
        #reset loading part
        time.sleep(2)
        container.write("")
        calculating_loading.write("")

    # st.write(
    #     f"""
    #     ## Session state:
    #     {st.session_state["source"]=}

    #     {st.session_state["target"]=}

    #     {st.session_state["button_check_source"]=}

    #     {st.session_state["button_confirm_source"]=}

    #     {st.session_state["button_check_target"]=}

    #     {st.session_state["button_confirm_target"]=}

    #     """
    # )
        




def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    # for key, value in islice(people.items(), 5):
    #     print(f"{type(key)}: {value}")
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

def shortest_path(source, target, node_explore_show):
    """
    Returns the shortest list of (movie_id, person_id) pairs 
    that connect the source to the target.

    If no possible path, returns None.


    (can be [(movie_id, person_id), (movie_id, person_id)]) => [(actoin,state)]
    """
    # print(type(source), type(target))
    number_of_explored = 0
    start_node = Node(state=source, parent=None,action=None)
    goal_node = Node(state=target, parent=None, action=None)

    frontier = QueueFrontier()
    frontier.add(start_node)

    explored = set()

    while True:
        if directory == "large":
            if number_of_explored % 5 == 0:
                node_explore_show.markdown(f'<span style="font-size:50px">Explore: {number_of_explored}</span>',unsafe_allow_html=True)
            elif number_of_explored <= 10:
                node_explore_show.markdown(f'<span style="font-size:50px">Explore: {number_of_explored}</span>',unsafe_allow_html=True)
                time.sleep(0.1)
        else:
            node_explore_show.markdown(f'<span style="font-size:50px">Explore: {number_of_explored}</span>',unsafe_allow_html=True)
            time.sleep(0.2)

        # print(number_of_explored)
        # node_explore_show.markdown(f'<span style="font-size:50px">Explore: {number_of_explored}</span>',unsafe_allow_html=True)
        if frontier.empty():
            return None # meaning both source and target are not connected
        
        node = frontier.remove() # FIFO method 
        number_of_explored += 1

        if node.state == goal_node.state:
            print("final state meet")
            paths = []
            while node.parent is not None:
                print("append something?")
                path = (node.action, node.state)
                # print(path)
                paths.append(path)
                node = node.parent
                # final print of explore
                node_explore_show.markdown(f'<span style="font-size:50px">Explore: {number_of_explored}</span>',unsafe_allow_html=True)

            paths.reverse()
            return paths
        
        explored.add(node.state)
        # print(f"node state: {node.state}")

        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                new_node = Node(state=state, parent=node, action=action)
                frontier.add(new_node)

def person_id_for_name(name):
    person_ids = list(names.get(name.lower(), set()))

    if len(person_ids) == 0:
        return None
    elif len(person_ids) == 1:
        return person_ids[0]
    else:
        # print(person_ids)
        people_list = [{"person_id": person_id,"name": people[person_id]["name"], "birth": people[person_id]["birth"]} for person_id in person_ids]
        return people_list
    

    

if __name__ == "__main__":
    main()