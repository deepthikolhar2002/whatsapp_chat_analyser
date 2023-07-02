import pandas as pd
import streamlit as st
import prerocessor
import helper
import matplotlib.pyplot as plt
st.sidebar.title('whatsapp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=prerocessor.preprocessor(data)

    # st.dataframe(df)

    user_list=df['user'].unique().tolist()

    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"overall")

    selected_user=st.sidebar.selectbox("show analysis wrt", user_list)

    if st.sidebar.button("SHOW ANALYSIS"):
        num_messages,words,num_media,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        #onthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['just_date'],daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color="yellow")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        if selected_user=="overall":
            st.title("most busy user")
            x,new_df=helper.most_busy_users(df)
            fig,ax =plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

    st.title("WorldCloud")
    df_wc=helper.create_word_cloud(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    most_comman_df=helper.most_comman_word(selected_user,df)
    fig, ax = plt.subplots()
    ax.barh(most_comman_df[0],most_comman_df[1])
    plt.xticks(rotation='vertical')
    st.title("most comman words")
    st.pyplot(fig)

    st.dataframe(most_comman_df)

    emoji_df=helper.emoji_helper(selected_user,df)
    st.title("Emoji Analysis")
    col1, col2 = st.columns(2)
    with col1:
       st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%0.2f')
        st.pyplot(fig)




