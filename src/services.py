def generate_results_and_save_matches(matches):
    [match.end_match() for match in matches]
    [match.save().execute() for match in matches]
