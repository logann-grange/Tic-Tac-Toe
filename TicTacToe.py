import math
import pygame
import time

difficulty = 3
is_multiplayer = False
is_computer = False

def change_difficulty(difficulty) :
    if difficulty + 1 <= 3 :
        screen.blit(pygame.image.load(f'assets/images/difficulty{difficulty+1}.png'), (0, 0))
        pygame.display.flip()
        return difficulty + 1
    else :
        screen.blit(pygame.image.load(f'assets/images/difficulty1.png'), (0, 0))
        pygame.display.flip()
        return 1
    

def print_info(signe, is_win, is_full) :
    screen.blit(img_info_fond, (119,737))
    if is_full :
        screen.blit(img_egalite, (180,740))
    elif is_computer and not is_win and signe == 'X' :
        screen.blit(img_votre_tour, (140,740))
    elif is_computer and not is_win and signe == 'O' :
        screen.blit(img_tour_ia, (180,740))
    elif is_computer and is_win and signe == 'O' :
        screen.blit(img_perdu, (120, 745))
    elif is_computer and is_win and signe == 'X' :
        screen.blit(img_gagne, (125, 745))
    elif is_computer and is_full :
        screen.blit(img_egalite, (180, 740))
    elif is_multiplayer and not is_win and signe == 'X' :
        screen.blit(img_tour_j1, (118, 740))
    elif is_multiplayer and not is_win and signe =='O' :
        screen.blit(img_tour_j2, (118,740))
    elif is_multiplayer and is_win and signe == 'X' :
        screen.blit(img_j1_gagne, (180,740))
    elif is_multiplayer and is_win and signe == 'O' :
        screen.blit(img_j2_gagne, (180, 740))
    pygame.display.flip()
        

def change_signe(signe_joueur) :
    if signe_joueur == "X" :
        print(signe_joueur)
        print_info("O", False, False)
        return "O"
    else : 
        print(signe_joueur)
        print_info("X", False, False)
        return "X"


def print_board(board):
    for i in range(3) :
        for j in range(3) :
            if board[i][j] == "X" :
                screen.blit(signe_x,(j*355/3+125, i*365/3+365))
                pygame.display.flip()
            elif board[i][j] == "O" :                                
                screen.blit(signe_o,(j*335/3+125+20, i*365/3+365-10))
                pygame.display.flip()

def play_sound(signe) :
    if signe == "X" :
        son_epees.play()
    else : 
        son_bouclier.play()


def is_winner(board, signe):
    # Vérifie les lignes
    for row in board:
        if all(cell == signe for cell in row):
            return True

    # Vérifie les colonnes
    for col in range(3):
        if all(board[row][col] == signe for row in range(3)):
            return True

    # Vérifie les diagonales
    if all(board[i][i] == signe for i in range(3)):
        return True
    if all(board[i][2 - i] == signe for i in range(3)):
        return True
    
    return False


def is_full(board):
    return all(cell != ' '  for row in board for cell in row)


def tour_joueur(index, board, signe) :
    if board[int(index[0])][int(index[1])] == ' ' :
        board[int(index[0])][int(index[1])] = signe
        print_board(board)
    return board


def minimax(board, depth, is_ia_turn):
    #Cas de base : si la partie est terminée, on renvoie le score
    if is_winner(board, 'O'):
        return 1      # Victoire de l’IA
    if difficulty > 1:
        if is_winner(board, 'X'):
            return -1     # Victoire du joueur
    if is_full(board):
        return 0      # Match nul

    #Si c’est le tour de l’IA (elle cherche le meilleur score possible)
    if is_ia_turn:
        best_score = -math.inf  # On part du plus petit score possible
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':  # Case libre
                    board[i][j] = 'O'   # L’IA joue ici
                    score = minimax(board, depth + 1, False)  # On simule la suite du jeu
                    board[i][j] = ' '   # On annule le coup
                    best_score = max(score, best_score)  # On garde le meilleur résultat
        return best_score

    #Si c’est le tour du joueur humain (il cherche à minimiser le score)
    else:
        best_score = math.inf  # On part du plus grand score possible
        if depth < difficulty :
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'   # Le joueur joue ici
                        score = minimax(board, depth + 1, True)  # On simule le tour suivant
                        board[i][j] = ' '   # On annule le coup
                        best_score = min(score, best_score)  # On garde le pire résultat pour l’IA
        return best_score


def best_move(board):
    
    best_score = -math.inf
    move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                # On simule un coup de l’IA
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ' '  # On annule le coup

                # Si le coup est meilleur que les précédents, on le garde
                if score > best_score:
                    best_score = score
                    move = (i, j)
    print(move)

    return move  # Retourne les coordonnées du meilleur coup


#initialisation de pygame
pygame.init()
pygame.mixer.init()

#import des images
background = pygame.image.load ('assets/images/grille.png')
menu = pygame.image.load('assets/images/menu.png')
signe_x = pygame.image.load ('assets/images/img_épées.png')
signe_o = pygame.image.load ('assets/images/img_bouclier.png')
img_info_fond = pygame.image.load('assets/images/fond_info.png')
img_votre_tour = pygame.image.load('assets/images/votre_tour.png')
img_tour_ia = pygame.image.load('assets/images/tour_ia.png')
img_tour_j1 = pygame.image.load('assets/images/tour_j1.png')
img_tour_j2 = pygame.image.load('assets/images/tour_j2.png')
img_difficulty3 = pygame.image.load('assets/images/difficulty3.png')
img_difficulty2 = pygame.image.load('assets/images/difficulty2.png')
img_difficulty1 = pygame.image.load('assets/images/difficulty1.png')
img_gagne = pygame.image.load('assets/images/gagne.png')
img_perdu = pygame.image.load('assets/images/perdu.png')
img_egalite = pygame.image.load('assets/images/égalité.png')
img_j1_gagne = pygame.image.load('assets/images/j1_gagne.png')
img_j2_gagne = pygame.image.load('assets/images/j2_gagne.png')

#import des sons
son_epees = pygame.mixer.Sound("assets/sons/son_épées.wav")
son_epees.set_volume(0.5)
son_bouclier = pygame.mixer.Sound("assets/sons/son_bouclier.wav")
son_bouclier.set_volume(0.5)
son_menu = pygame.mixer.Sound("assets/sons/son_menu.mp3")
music_fond = pygame.mixer.music.load("assets/sons/musique_fond.mp3")
pygame.mixer.music.play(-1)

#def des Boutons :
bouton_00 = pygame.Rect(125,365, 111, 111)
bouton_01 = pygame.Rect(240,365, 111, 111)
bouton_02 = pygame.Rect(365, 365, 111, 111)
bouton_10 = pygame.Rect(125, 480, 111, 111)
bouton_11 = pygame.Rect(240, 480, 111, 111)
bouton_12 = pygame.Rect(365, 480, 111, 111)
bouton_20 = pygame.Rect(125, 600, 111, 111)
bouton_21 = pygame.Rect(240, 600, 111, 111)
bouton_22 = pygame.Rect(365, 600, 111, 111)

board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
screen = pygame.display.set_mode((600, 800))
signe_joueur = "X"
signe_ia = "O"
signe_actuel = signe_joueur
is_running = True
is_menu = True
is_game = True


while is_running :

    #menu du jeu
    while is_menu :
        screen.blit(menu, (0,0))
        screen.blit(pygame.image.load(f'assets/images/difficulty{difficulty}.png'), (190+ (3-difficulty)*25, 740))
        pygame.display.flip()
        bouton_computer = pygame.Rect(75, 280, 445, 190)
        bouton_multiplayer = pygame.Rect(75, 490, 445, 130)
        bouton_diff = pygame.Rect(75, 650, 445, 120)
        #pygame.display.flip() 
        
        for event in pygame.event.get() :
            if event.type == pygame.MOUSEBUTTONUP :
                if event.button == 1: # 1= clique gauche
                    son_menu.play()
                    if bouton_diff.collidepoint(event.pos) :
                        difficulty = change_difficulty(difficulty)
                        print("diff: ", difficulty)
                    elif bouton_multiplayer.collidepoint(event.pos) :
                        print("multi")
                        is_menu = False
                        is_multiplayer = True
                    elif bouton_computer.collidepoint(event.pos) :
                        is_menu = False
                        is_computer = True

        if event.type == pygame.QUIT:
                is_running = False
                tour_fini = True
                pygame.quit()

    #while is_game == True :
    screen.blit(background,(0, 0))
    print_board(board)

    #affichage des infos sur la pancarte
    if is_computer :
        print_info(signe_actuel, is_winner(board, 'X') or is_winner(board, 'O'), is_full(board))
    else :
        print_info(signe_joueur, is_winner(board, 'X') or is_winner(board, 'O'), is_full(board))

    pygame.display.flip()
    tour_fini = False
    while not tour_fini :
        for event in pygame.event.get() :
            if event.type == pygame.MOUSEBUTTONUP: #s'active quand clic laché
                if event.button == 1 and is_game : # 1= clique gauche
                    play_sound(signe_joueur)
                    if bouton_00.collidepoint(event.pos) :
                        board = tour_joueur("00", board, signe_joueur)
                        print (board, signe_joueur)
                        tour_fini = True
                    if bouton_01.collidepoint(event.pos) :
                        board = tour_joueur("01", board, signe_joueur)
                        print(board, signe_joueur)
                        tour_fini = True
                    if bouton_02.collidepoint(event.pos) :
                        board = tour_joueur("02", board, signe_joueur)
                        print(board, signe_joueur)
                        tour_fini = True
                    if bouton_10.collidepoint(event.pos) :
                        board = tour_joueur("10", board, signe_joueur)
                        print(board, signe_joueur)
                        tour_fini = True
                    if bouton_11.collidepoint(event.pos) :
                        board = tour_joueur("11", board, signe_joueur)
                        print(board, signe_joueur)
                        tour_fini = True
                    if bouton_12.collidepoint(event.pos) :
                        board = tour_joueur("12", board, signe_joueur)
                        print(board, signe_joueur)
                        tour_fini = True
                    if bouton_20.collidepoint(event.pos) :
                        board = tour_joueur("20", board, signe_joueur)
                        print(board, signe_joueur)
                        tour_fini = True
                    if bouton_21.collidepoint(event.pos) :
                        board = tour_joueur("21", board, signe_joueur)
                        print(board)
                        tour_fini = True
                    if bouton_22.collidepoint(event.pos) :
                        board = tour_joueur("22", board, signe_joueur)
                        print(board)
                        tour_fini = True

            if event.type == pygame.QUIT:
                is_running = False
                tour_fini = True
                pygame.quit()

    if is_multiplayer and not is_winner(board, signe_joueur):
        signe_joueur = change_signe(signe_joueur)

    if is_computer and not is_winner(board, "X") and not is_full(board) :
        print_info('O', False, False)
        time.sleep(1)
        # L’IA choisit le meilleur coup
        move = best_move(board)
        # On applique le coup si disponible
        if move:
            board[move[0]][move[1]] = 'O'
        print_board(board)
        play_sound(signe_ia)
        
    elif is_winner(board, "X") :
        print("Partie terminée : vous avez gagné !")
        print_info(signe_joueur, True, False)
        is_game = False

    elif is_full(board) :
        print("Partie terminée : Egalité !")
        print_info(signe_joueur, False, True)
        is_game = False


    if is_winner(board, signe_ia) :
        print("Partie terminée : vous avez perdu !")
        print_info(signe_ia, True, False)
        signe_actuel = signe_ia
        is_game = False


    pygame.display.flip()

pygame.mixer.music.stop()