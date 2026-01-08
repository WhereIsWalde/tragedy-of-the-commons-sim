import streamlit as st
import st_util as util
import time

is_admin: bool = st.query_params.get("role") == "admin"
if "game" not in st.session_state:
    st.session_state["game"] = util.get_global_game()
#http://localhost:8501/?role=admin

if is_admin:
    st.sidebar.header("Admin Panel")
    with st.sidebar:
        st.write(f"### 👥 Players Joined: {st.session_state.game.N}")
        if st.button("Play Game"):
            st.session_state.game.play()
            st.write(st.session_state.game.is_finished)
        

with st.container(border=True): 
    st.markdown(r"""
    ###  Tragedy of the Commons Simulator

    **You are the leader of a goods factory.** You are faced with a decision of how much to produce. 
                
    But you are not the only one. There are $N$ different factories around the world facing a similar decision!

    ---

    ####  The Rules

    1.  **📦 Production ($x$):** You choose to produce $x \in \{1,2,3,4,5\}$ tons of goods.
    2.  **💨 Emissions ($e$):** 1 ton of goods = 1 ton of emissions.
    3.  **💰 Base Utility ($u$):** You earn 1 point per ton produced.

    However, if the environment is ruined, you can't enjoy your hard-earned money! Your total utility is calculated as:

    $$
    U = \left( 1 - \frac{\sum_{i=1}^N e_i}{5N} \right) u
    $$

    Your base utility is lowered by the emissions of **each player** in the game. If every player chooses to produce the full 5 tons, the whole planet is ruined and everyone gets **0 utility**.

    **How many goods will you produce to maximize your utility? How about everyone's total utility?**
    """)

if not st.session_state.get("has_submitted", False):
    with st.form(border=True, key="decision"):
        factory_name = st.text_input("Please input the name of your factory:")
        goods_produced = st.number_input("Please input tons of goods to produce: ",1,5,1,1)
        if st.form_submit_button():
            if "has_submitted" not in st.session_state:
                st.session_state.game.add_player(factory_name=factory_name, amount_produced=goods_produced)
                st.session_state["has_submitted"] = True
                st.success("Your factory was saved to the game!")
                if "factory_name" not in st.session_state:
                    st.session_state["factory_name"] = factory_name
                time.sleep(2.0)
                st.rerun()

else:
    @st.fragment(run_every=3)
    def output_screen():
        # Case A: Game is finished, show results
        if st.session_state.game.is_finished:
            my_name = st.session_state.get("factory_name")

            if my_name and my_name in st.session_state.game.player_utilities:
                my_utility = st.session_state.game.player_utilities[my_name]
                my_production = st.session_state.game.player_choices[my_name]
                my_emissions = st.session_state.game.player_emissions[my_name]

                mean_utility = st.session_state.game.get_mean_utility()
                median_utility = st.session_state.game.get_median_utility()
                total_utility = st.session_state.game.get_total_utility()
                max_utility = st.session_state.game.get_theoretic_maximum_utility()
                chart = util.get_choice_histogram(st.session_state.game.player_choices)

                with st.container(border=True):
                    st.header("Results")
                    st.write(f"You produced: {my_production} tons, creating {my_emissions} tons of emissions!")
                    with st.container(horizontal=True):
                        st.metric(label=f"Utility for {my_name}:", value=f"{my_utility:.2f} Utility", delta=f"{my_utility-mean_utility:.2f}")
                        st.metric(label=f"Mean Utility:", value=f"{mean_utility:.2f} Utility")
                        st.metric(label=f"Median Utility:", value=f"{median_utility:.2f} Utility")
                    with st.container(horizontal=True):
                        st.metric("Global utility:",value=f"{total_utility:.2f} Utility")
                        st.metric("Theoretical maximum utility:", value=f"{max_utility:.2f} Utility")
                    st.plotly_chart(chart, use_container_width=True)
                    

                        
            else:
                st.warning("You didn't participate in this round.")
                
        # Case B: Game is in Lobby, show input form
        else:
            st.info(f"Waiting for the game to begin, current number of players: {st.session_state.game.N}")

    output_screen()
        

# streamlit run run.py