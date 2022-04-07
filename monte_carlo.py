from attr import asdict
import numpy as np
import random
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import statistics
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Monte Carlo Simulation Demo", anchor=None)
st.subheader("Gambling 'game'")


st.write("Play the game by 'rolling' a 100-sided die (select parameters from left pane).")
st.write('If you a roll number between 51 and 99, you WIN.')
st.write('Any number less than 50, you LOSE.')
st.write('If you roll an even 100, the house WINS and you LOSE.')
st.write('You have a 49% chance of winning each roll of the die. ')
st.write('If you lose your initial funds, the house will issue you a line of credit (so play carefully!)')
st.write('Continue by selecting the i) the initial funds per player ii) the bet each player will be placing per round iii) the number of games to play and iv) the number of players around the table.')
st.write('Good luck!')


add_slider1 = st.sidebar.slider('Select initial funds', 100, 2000, 1000)
add_slider2 = st.sidebar.slider('Place bet', 100, 500, 200)
add_slider3 = st.sidebar.slider('Select number of games to play (simulations)', 1, 50000, 500)
add_slider4 = st.sidebar.slider('Select number of players to include in monte carlo simulation', 1, 500, 100)

x_element = int(add_slider4)


def rollDice():
    roll = random.randint(1,100)

    if roll == 100 or roll <= 50:
        return False
    else:
        return True


values_list = []

def simple_bettor(intitial_funds,initial_bet,game_count):
    """"
    Function takes the following parameters: 
    - intitial_funds = account balance at start
    - Initial_bet = Initial bet to be gambled
    - game_count = Number of games player wishes to play

    """
    account_balance = intitial_funds
    bet = initial_bet
    global values_list
    wX = []
    vY = []

    # initialize games variable for while-loop
    games = 1

    while games <= game_count:
        if rollDice(): # if True
            account_balance += bet
            wX.append(games)
            vY.append(account_balance)
            values_list.append(account_balance)

        else:
            account_balance -= bet
            wX.append(games)
            vY.append(account_balance)
            values_list.append(account_balance)
        
        games += 1 # add 1 game played to "game" variable
    #print(f'Player Account Balance: {account_balance} $')
    plt.plot(wX,vY)


st.subheader('Monte Carlo simulation')

st.write('The chart below demonstrates a Monte Carlo simulation of ',add_slider4,'individual players and ',add_slider3, ' simulations (games) with a bet of: ', add_slider2, '/game/player and', add_slider1, '$ of initial funds/game/player. The y-axis demonstrates each players cumulative closing balance.')


num_players = add_slider4
x = 0
while x < num_players:
    simple_bettor(add_slider1,add_slider2,add_slider3)
    x += 1


plt.ylabel('Account balance')
plt.xlabel('Number of games (simulations)')
fig = plt.show()
st.pyplot(fig)


chuncks = np.array_split(values_list, x_element)

best_player = []
worst_player = []
other_data = []

for chunck in chuncks:
    best_player.append(max(chunck[-1:]))
    worst_player.append(min(chunck[-1:]))
    other_data.append(chunck[-1:])

med = np.median(values_list)
hi = max(values_list)
lo = min(values_list)
ave = np.average(values_list)
list_len = len(values_list)


st.subheader('Results (closing balance, best and worst player)')

st.write('Highest closing balance', max(best_player))
st.write('Lowest closing balance', min(worst_player))
st.write('Median closing balance', np.median(other_data))
st.write('Average closing balance', np.average(other_data))


st.subheader('Results (complete simulation, all players)')

st.write('Median', med)
st.write('Highest account balance at any given simulation', hi)
st.write('Lowest account balance at any given simulation', lo)
st.write('Average account balance', np.average(values_list))





hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 