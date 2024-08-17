import pandas as pd
pd.set_option('display.max_colwidth', None)

df = pd.read_csv("jeopardy.csv")
print(df.columns)

def filter_questions_by_words(df, words):
    filter_condition = df[' Question'].str.contains('|'.join(words), case=False, na=False)
    for word in words:
        filter_condition &= df[' Question'].str.contains(word, case=False, na=False)
    return df[filter_condition]

filtered_df = filter_questions_by_words(df, ["viking", "england"])
print(filtered_df)

def convert_value_to_float(df):
    # Replace dollar signs and commas, handle missing values, and convert to float
    df['Value (Float)'] = df[' Value'].replace('[\$,]', '', regex=True)
    
    # Convert to numeric, coercing errors to NaN
    df['Value (Float)'] = pd.to_numeric(df['Value (Float)'], errors='coerce')
    
    return df

# Example usage
df = convert_value_to_float(df)
print(df[[' Value', 'Value (Float)']].head())

def count_unique_answers(df, keyword):
    # Filter questions containing the keyword
    filtered_df = df[df[' Question'].str.contains(keyword, case=False, na=False)]
    # Count unique answers and their occurrences
    answer_counts = filtered_df[' Answer'].value_counts()
    return answer_counts
# Example usage
keyword_answers = count_unique_answers(df, "King")
print(keyword_answers)

def count_keyword_by_decade(df, keyword, start_year, end_year):
    # Convert ' Air Date' to datetime
    df[' Air Date'] = pd.to_datetime(df[' Air Date'])
    
    # Filter questions by the specified decade
    decade_df = df[(df[' Air Date'].dt.year >= start_year) & (df[' Air Date'].dt.year <= end_year)]
    
    # Count the occurrences of the keyword in the ' Question' column
    keyword_count = decade_df[' Question'].str.contains(keyword, case=False, na=False).sum()
    
    return keyword_count

# Example usage: Compare the word "Computer" in the 90s and 2000s
count_90s = count_keyword_by_decade(df, "Computer", 1990, 1999)
count_2000s = count_keyword_by_decade(df, "Computer", 2000, 2009)

print(f"Number of 'Computer' questions in the 90s: {count_90s}")
print(f"Number of 'Computer' questions in the 2000s: {count_2000s}")

def round_category_analysis(df):
    # Group by ' Round' and ' Category' and count occurrences
    round_category_counts = df.groupby([' Round', ' Category']).size().unstack().fillna(0)
    
    return round_category_counts

# Example usage: Analyze the connection between round and category
round_category_df = round_category_analysis(df)

# Display categories that appear most often in each round
print(round_category_df.idxmax(axis=1))  # This will show the most common category for each round

import random

def quiz_yourself(df):
    while True:
        # Grab a random question
        random_row = df.sample(n=1).iloc[0]
        question = random_row[' Question']
        correct_answer = random_row[' Answer']
        
        # Ask the question
        user_answer = input(f"Question: {question}\nYour Answer: ")
        
        # Check if the answer is correct
        if user_answer.strip().lower() == correct_answer.strip().lower():
            print("Correct!")
        else:
            print(f"Wrong. The correct answer was: {correct_answer}")
        
        # Ask if they want to play again
        play_again = input("Do you want to try another question? (yes/no): ")
        if play_again.strip().lower() != 'yes':
            break

# Example usage: Start the quiz
quiz_yourself(df)