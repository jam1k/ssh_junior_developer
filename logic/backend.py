# tic_tac_toe/logic/backend.py
from flask import Flask, request, jsonify
import uuid

from validators import (
    check_initial_grid, validate_board, get_starting_mark, get_mark_other, 
    validate_game_state, validate_difference_1char_allowed, get_empty_count, get_winner
    )

from exceptions import InvalidGameState
from tic_tac_toe import play_game_backend

app = Flask(__name__)
games_container= []

@app.route('/api/v1/games', methods=['GET', 'POST'])
def games():
    # for this exercise only I created a global varaible.
    # As next step it would be possible to store all games in DB.
    # From DB it is easier to select a view for GET response.

    global games_container 
    if request.method == "GET":
        all_games = []
        for item in games_container:
            all_games.append({key: item[key] for key in item.keys()&{"id", "board", "status"}})
        return all_games, 200

    if request.method == "POST":
        try:
            board = request.json
        except:
            return {"reason": "Board not found"}, 404
        try:
            validate_board(board)
            check_initial_grid(board["board"])
        except InvalidGameState as e:
            return jsonify({"reason":e.error}), 400
        
        game_id = str(uuid.uuid4())
        starting_mark = get_starting_mark(board["board"])

        game_dict = {}        
        game_dict["id"] = game_id
        game_dict["board"] = board["board"]
        game_dict["status"] = "RUNNING"        
        game_dict["starting_mark"] = starting_mark
        game_dict["winner"] = None

        if get_empty_count(board["board"]) == 9: 
            #Denote computer mark if the board is empty
            game_dict["computer_mark"] = "X"
        else:
            game_dict["computer_mark"] = get_mark_other(starting_mark)

        try: 
            # Make a first computer move
            play_game_backend(game_dict)
        except InvalidGameState as e:
            return jsonify({"reason": e.error}), 400

        games_container.append(game_dict)

        url_address = {}
        url_address["location"] = request.base_url+"/"+game_id
        return url_address, 201

@app.route('/api/v1/games/<game_id>', methods=['GET', 'PUT', 'DELETE'])
def game(game_id):
    if request.method == "GET":
        for item in games_container:
            if item["id"] == game_id:
                return item, 200    
        return {"reason": "game not found"}, 404
        
    if request.method == "PUT":
        new_board = request.json
        try:
            validate_board(new_board)
        except InvalidGameState as e:
            return jsonify({"reason":e.error}), 400
        
        for item in games_container:
            if item["id"] == game_id:
                try:
                    validate_difference_1char_allowed(item["board"], new_board["board"])
                    validate_game_state(new_board["board"], item["starting_mark"])
                except InvalidGameState as e:
                    return jsonify({"reason":e.error}), 400
                if item["status"] == "FINISHED":
                    return {"reason": "Game is finnished!"}, 400
                
                item["board"] = new_board["board"]

                try:                    
                    item = play_game_backend(item)
                except InvalidGameState as e:
                    return jsonify({"reason":e.error}), 400                

                if item["status"] == "FINISHED":
                    if item["winner"] == "Tie":
                        return {"reason": "Tie, try next time"}
                    else:
                        return {"reason": item["winner"]+"  has won"}
                else:
                    return item

        return {"reason": "game not found"}, 404

    if request.method == "DELETE":
        for item in games_container:
            if item["id"] == game_id:
                games_container.remove(item)
                return {'message': 'Game successfully deleted'}, 200
        return {'message': 'Game with provided ID not found'}, 404

if __name__ == "__main__":    
    app.run(debug=True)