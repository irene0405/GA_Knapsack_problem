#include <iostream>
#include <fstream>
#include <random>
#include <cstring>
#include <iomanip>
#include <chrono>

#define ROUND 100
#define GENERATION 100
#define POPULATION 100
#define CROSSOVER_RATE 0.5
#define MUTATION_RATE 0.5
#define MUTATE_POINT 1  // The number of the mutate point

using namespace std;

typedef struct Individuals {
    int gene[100];
    int weight;
    int fitness;
} Individuals;

Individuals individual[POPULATION];
Individuals pool[POPULATION];
Individuals best;

int random(int start, int end) {
    random_device rd;
    default_random_engine gen = default_random_engine(rd());
    uniform_int_distribution<int> dis(start, end);
    return dis(gen);
}

void initialize() {
    for (int i = 0; i < POPULATION; i++) {
        individual[i].weight = 0;
        individual[i].fitness = 0;
        pool[i].weight = 0;
        pool[i].fitness = 0;
        for (int j = 0; j < 100; j++) {
            individual[i].gene[j] = random(0, 1);
            pool[i].gene[j] = 0;
        }
    }
    for (int i = 0; i < 100; i++) {
        best.gene[i] = 0;
    }
    best.weight = 0;
    best.fitness = 0;
}

void calcFitness() {
    for (int i = 0; i < POPULATION; i++) {
        individual[i].weight = 0;
        individual[i].fitness = 0;
        int weight = 0;
        int value = weight + 5;
        for (int j = 0; j < 100; j++) {
            if (j % 10 == 0) {
                weight++;
                value++;
            }
            if (individual[i].gene[j] == 1) {
                individual[i].weight += weight;
                individual[i].fitness += value;
            }
        }

        if (individual[i].weight > 275) {
            for (int j = 99; j >= 0; j--) {
                if (individual[i].gene[j] == 1) {
                    individual[i].gene[j] = 0;
                    if (j > 89) {
                        individual[i].weight -= 10;
                        individual[i].fitness -= 15;
                    } else if (j > 79) {
                        individual[i].weight -= 9;
                        individual[i].fitness -= 14;
                    } else if (j > 69) {
                        individual[i].weight -= 8;
                        individual[i].fitness -= 13;
                    } else if (j > 59) {
                        individual[i].weight -= 7;
                        individual[i].fitness -= 12;
                    } else if (j > 49) {
                        individual[i].weight -= 6;
                        individual[i].fitness -= 11;
                    } else if (j > 39) {
                        individual[i].weight -= 5;
                        individual[i].fitness -= 10;
                    } else if (j > 29) {
                        individual[i].weight -= 4;
                        individual[i].fitness -= 9;
                    } else if (j > 19) {
                        individual[i].weight -= 3;
                        individual[i].fitness -= 8;
                    } else if (j > 9) {
                        individual[i].weight -= 2;
                        individual[i].fitness -= 7;
                    } else {
                        individual[i].weight -= 1;
                        individual[i].fitness -= 6;
                    }
                    if (individual[i].weight <= 275)
                        break;
                }
            }
        }

        if (individual[i].fitness > best.fitness) {
            memcpy(&best, &individual[i], sizeof(best));
        }
    }
}

void select() {
    int i1, i2;
    for (int i = 0; i < POPULATION; i++) {
        i1 = random(0, POPULATION - 1);
        do {
            i2 = random(0, POPULATION - 1);
        } while (i1 == i2);
        if (individual[i1].fitness > individual[i2].fitness) {
            memcpy(&pool[i], &individual[i1], sizeof(pool[i]));
        } else {
            memcpy(&pool[i], &individual[i2], sizeof(pool[i]));
        }
    }
}

void crossover() {
    int i1, i2;
    for (int i = 0; i < POPULATION; i += 2) {
        if ((random(0, 100) / 100.0) > CROSSOVER_RATE) {
            continue;
        }

        i1 = random(0, POPULATION - 1);
        do {
            i2 = random(0, POPULATION - 1);
        } while (i1 == i2);

        int crossoverPosition = random(0, 99);
        for (int j = 0; j < 100; j++) {
            if (j < crossoverPosition) {
                individual[i].gene[j] = pool[i1].gene[j];
                individual[i + 1].gene[j] = pool[i2].gene[j];
            } else {
                individual[i].gene[j] = pool[i2].gene[j];
                individual[i + 1].gene[j] = pool[i1].gene[j];
            }
        }
    }
}

void mutate() {
    int position;
    for (int i = 0; i < POPULATION; i++) {
        if (((random(0, 100) / 100.0)) > MUTATION_RATE) {
            continue;
        }
        for (int j = 0; j < MUTATE_POINT; j++) {
            position = random(0, 99);
            individual[i].gene[position] = 1 - individual[i].gene[position];
        }
    }
}

int main() {
    int count_620 = 0, count_615 = 0, count_610 = 0, count_605 = 0, count_600 = 0, count_under_600 = 0;
    int best_value = INT_MIN, worst_value = INT_MAX, total = 0;

    // count execution time
    auto start = chrono::steady_clock::now();

    ofstream ofs;
    ofs.open("output.txt");
    ofs << "Round: " << ROUND << endl;
    ofs << "Generation: " << GENERATION << endl;
    ofs << "Population: " << POPULATION << endl;
    ofs << "Crossover rate: " << CROSSOVER_RATE << endl;
    ofs << "Mutation rate: " << MUTATION_RATE << endl;
    ofs << "Mutation type: " << MUTATE_POINT << " point(s)" << endl;
    ofs << "============================" << endl;

    for (int j = 0; j < ROUND; j++) {
        initialize();
        for (int i = 0; i < GENERATION; i++) {
            calcFitness();
            select();
            crossover();
            mutate();
        }

        if (best.fitness == 620) {
            count_620++;
        } else if (best.fitness >= 615 && best.fitness < 620) {
            count_615++;
        } else if (best.fitness >= 610 && best.fitness < 615) {
            count_610++;
        } else if (best.fitness >= 605 && best.fitness < 610) {
            count_605++;
        } else if (best.fitness >= 600 && best.fitness < 605) {
            count_600++;
        } else {
            count_under_600++;
        }
        total += best.fitness;
        if (best.fitness > best_value) {
            best_value = best.fitness;
        } else if (best.fitness < worst_value) {
            worst_value = best.fitness;
        }
        ofs << "Round: " << j + 1 << " / " << ROUND << " --- " << best.fitness << endl;
    }
    ofs << "============================" << endl;
    ofs << "      620 :" << setw(3) << count_620 << " time(s)" << endl;
    ofs << "[615, 620):" << setw(3) << count_615 << " time(s)" << endl;
    ofs << "[610, 615):" << setw(3) << count_610 << " time(s)" << endl;
    ofs << "[605, 610):" << setw(3) << count_605 << " time(s)" << endl;
    ofs << "[600, 605):" << setw(3) << count_600 << " time(s)" << endl;
    ofs << "under 600 :" << setw(3) << count_under_600 << " time(s)" << endl;
    ofs << "============================" << endl;
    ofs << "Average value: " << (float) total / ROUND << endl;
    ofs << "Worst value: " << worst_value << endl;
    ofs << "Best value: " << best_value << endl;
    ofs << "============================" << endl;

    // count execution time
    auto end = chrono::steady_clock::now();
    cout << "Time taken: " << chrono::duration<double>(end - start).count() << " s" << endl;

    ofs << "Time taken: " << chrono::duration<double>(end - start).count() << " s" << endl;
    ofs.close();
}