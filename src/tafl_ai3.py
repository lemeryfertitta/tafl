#!/usr/bin/env python
import tafl

def get_next_boards(current_board, player):
	player_pieces = []
	next_boards = []
	for piece in current_board.game_pieces:
		if piece.player == player or piece.player == (player+2):
			player_pieces.append(piece)
	for piece in player_pieces:
		piece_boards = (current_board.get_possible_next_boards( (piece.x,piece.y) ))
		for board in piece_boards:
			next_boards.append(board)
	return next_boards


def evaluate_board(current_board, player):
	winner = current_board.check_for_game_won()
	if winner == player:
		return 1
	elif winner != 0:
		return -1
	score = 0
	for piece in current_board.game_pieces:
		if piece.player == player:
			score += .05
		else:
			score -= .05
	return score

def minimax(current_player, maximizingPlayer, current_board, depth):
	if depth == 0 or (current_board.check_for_game_won() != 0):
		if not maximizingPlayer:
			return evaluate_board(current_board, current_player)
		else:
			return evaluate_board(current_board, current_player%2+1)
	next_boards = get_next_boards(current_board, current_player)
	if maximizingPlayer:
		bestValue = -10
		for board in next_boards:
			value = minimax(current_player%2+1,False, board, depth-1)
			bestValue = max(bestValue,value)
		return bestValue
	else:
		bestValue = 10
		for board in next_boards:
			value = minimax(current_player%2+1,True, board, depth-1)
			bestValue = min(bestValue,value)
		return bestValue

def alphabetaMinimax(current_player, maximizingPlayer, current_board, depth, alpha, beta):
	if depth == 0 or (current_board.check_for_game_won() != 0):
		if not maximizingPlayer:
			return evaluate_board(current_board, current_player)
		else:
			return evaluate_board(current_board, current_player%2+1)
	next_boards = get_next_boards(current_board, current_player)
	if maximizingPlayer:
		for board in next_boards:
			alpha = max(alpha, alphabetaMinimax(current_player%2+1,False, board, depth-1,alpha,beta))
			if beta <= alpha:
				break
		return alpha
	else:
		for board in next_boards:
			beta = min(beta, alphabetaMinimax(current_player%2+1,True, board, depth-1,alpha,beta))
			if beta <= alpha:
				break
		return beta

def negascout(current_player, colour, current_board, depth, alpha, beta):
	if depth == 0 or (current_board.check_for_game_won() != 0):
		if colour == -1:
			return colour * evaluate_board(current_board, current_player)
		else:
			return colour * evaluate_board(current_board, current_player%2+1)
	#next_boards = get_next_boards(current_board, current_player)
	next_boards = get_next_boards_Negascout(current_board, current_player)
	for board in next_boards:
		if board != next_boards[0]:
			score = -negascout(current_player%2+1, -colour, board, depth-1, -alpha-1, -alpha)
			if alpha < score and score < beta:
				score = -negascout(current_player%2+1, -colour, board, depth-1, -beta, -score)
		else:
			score = -negascout(current_player%2+1, -colour, board, depth-1, -beta, -alpha)
		alpha = max(alpha, score)
		if alpha >= beta:
			break
	return alpha

# this doesn't seem to beat regular "get_next_boards" but it should...
def get_next_boards_Negascout(current_board, player):
	player_pieces = []
	next_boards = []
	for piece in current_board.game_pieces:
		if piece.player == player or piece.player == (player+2):
			player_pieces.append(piece)
	for piece in player_pieces:
		piece_boards = (current_board.get_possible_next_boards( (piece.x,piece.y) ))
		for board in piece_boards:
			next_boards.append(board)
	best_score = -10
	best_index = 0
	index = 0
	for board in next_boards:
		score = evaluate_board(board, player)
		if score > best_score:
			best_score = score
			best_index = index
		index += 1
	next_boards[0], next_boards[best_index] = next_boards[best_index], next_boards[0]

	return next_boards


def get_move(current_board, player):
	next_boards = get_next_boards(current_board, player)
	best_score = -10
	for board in next_boards:
		#score = minimax(player%2+1, True, board, 2)
		score = alphabetaMinimax(player%2+1, True, board, 2, -1, 1)
		#score = negascout(player%2+1, 1, board, 2, -1, 1)
		if score > best_score:
			next_board = board
			best_score = score
	return next_board