# -*- coding: utf-8 -*-
# Retrait des logs
import os

# Bibliothque
import numpy as np
from Puissance4 import JeuPuissance4
from LogManager import LogManager
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras.utils import plot_model
from random import randrange, random, choice
from keras.utils.vis_utils import model_to_dot
from tensorflow.keras.optimizers.legacy import Adam


class IAPlayer:
    def __init__(self, save=None):
        self.epoch = 0
        self.epsilon = 0.4
        self.gamma = 0.9
        self.previousGrid = None
        self.previousMove = None

        # Création du modèle d'IA
        if save:
            print("[IAPlayer] Chargement du modèle")
            self.q = load_model(save)
        else:
            self.q = Sequential()
            self.q.add(Dense(64, activation="relu", input_dim=(6 * 7 * 3) + (7)))
            self.q.add(Dense(1, activation="relu"))
            optimizer = Adam()
            self.q.compile(optimizer=optimizer, loss="mean_squared_error")
        # plot_model(self.q,to_file="model.png")

    def predict(self, game: JeuPuissance4) -> int:
        """

        Parameters
        ----------
        grid : list
            Liste de liste avec 0, 1 ou 2 pour la grille du jeu

        Returns
        -------
        int
            Le numéro de colonne où il faut mettre le jeton

        """
        grid = game.grid
        self.previousGrid = tuple(grid)
        actions = game.possiblePlays()
        # Mutation générationnel
        if random() < self.EPSILON:
            self.previousMove = choice(actions)
            return self.previousMove
        # Choisir l'action avec le plus gros score
        QValues = [self.getQ(self.previousGrid, a) for a in actions]
        # print(QValues)
        maxQValue = max(QValues)
        # Si il y a plusieurs actions "bonnes" on choisi une solution aléatoire
        if QValues.count(maxQValue) > 1:
            bestActions = [i for i in range(len(actions)) if QValues[i] == maxQValue]
            bestMove = actions[choice(bestActions)]
        # SInon on prend l'action unique
        else:
            bestMove = actions[QValues.index(maxQValue)]
        self.previousMove = bestMove
        return self.previousMove

    def getQ(self, state, action):
        return self.q.predict([self.traiter(state, action)], verbose=0, batch_size=1)

    def generateReward(self, winner, game):
        """
        IA === Joueur 2
        """
        if winner == 2:
            return self.reward(10, game)
        elif winner == 1:
            return self.reward(-10, game)
        elif winner == 3:
            return self.reward(-3, game)
        else:
            return self.reward(0, game)

    def reward(self, value, game):
        """
        10  => Victoire
        -10 => Perd
        -3  => Match nul
        """
        board = game.grid
        prevPossiblePlays = game.possiblePlays(self.previousGrid)
        if self.previousMove and len(prevPossiblePlays) > 0:
            prevQ = self.getQ(self.previousGrid, self.previousMove)
            maxQnew = max([self.getQ(tuple(board), a) for a in prevPossiblePlays])
            print(
                self.traiter(self.previousGrid, self.previousMove),
                prevQ + 0.3 * ((value + self.gamma * maxQnew) - prevQ),
            )
            self.q.fit(
                self.traiter(self.previousGrid, self.previousMove),
                prevQ + 0.3 * ((value + self.gamma * maxQnew) - prevQ),
                epochs=1,
                verbose=0,
            )
        self.previousGrid = None
        self.previousMove = None
        return value

    def traiter(self, board, action):
        vector = []
        board = [item for sublist in board for item in sublist]
        u_board = [1, 0, 2]
        for b in board:
            for b_u in u_board:
                if b == b_u:
                    vector.append(1)
                else:
                    vector.append(0)
        for a in range(7):
            if action == a:
                vector.append(1)
            else:
                vector.append(0)
        output = np.array([vector])
        return output

    def train():
        """ """


if __name__ == "__main__":
    trainCycles = 200
    trainEpsilon = 0.4
    botWin = 0
    otherWin = 0
    ia_name = "faustin_1"

    print(
        f"[Trainer] Debut du train pour {trainCycles} cycles et {trainEpsilon} d'epsilon"
    )

    ia = IAPlayer()
    # another_ia = IAPlayer("ia_vs_ia")

    logManager = LogManager()
    logManager.openFile()

    ia.EPSILON = trainEpsilon
    # another_ia.EPSILON = 0

    lastGameSet = []
    for i in range(trainCycles):
        print(i)
        if i % 100 == 0:
            ia.q.save(ia_name)
            logManager.saveData(lastGameSet)
            lastGameSet = []
            pourcent = int((i / trainCycles) * 100)
            pourcent_win = int((botWin / i) * 100) if i > 0 else 0
            print(
                f"[Trainer] Avancement {pourcent}% / 100% - Pourcentage de victoire {pourcent_win}% / 100%"
            )

        game = JeuPuissance4()
        isFinish = False
        currentPlayer = 1
        while not isFinish:
            if currentPlayer == 1:
                while True:
                    result = game.play(randrange(7))
                    if result == 0:
                        continue
                    else:
                        currentPlayer = result[0]
                        isFinish = result[1]
                        break

            elif currentPlayer == 2:
                prediction = ia.predict(game)
                result = game.play(prediction)
                currentPlayer = result[0]
                isFinish = result[1]

        # Gestion fin de partie
        if isFinish == 1:
            otherWin += 1
        elif isFinish == 2:
            botWin += 1
        reward = ia.generateReward(isFinish, game)
        lastGameSet.append(
            {
                "grid": game.grid,
                "turns": game.turns,
                "isFinish": isFinish,
                "reward": reward,
            }
        )

    # Fin du programme de train
    pourcent_win = int((botWin / trainCycles) * 100)
    # ia.q.save(ia_name)
    logManager.saveData(lastGameSet)
    logManager.closeFile()
    print(
        f"[Trainer] Avancement 100% / 100% ! - Pourcentage de victoire {pourcent_win}% /100%"
    )
    print("[Trainer] Fin")

# Code Pour adversaire aléatoire
"""
prediction = another_ia.predict(game)
result = game.play(prediction)
currentPlayer = result[0]
isFinish = result[1]
"""
