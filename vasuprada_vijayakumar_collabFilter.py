import csv
import sys
import math
ratings_matrix = {}
movie_rated_user1 = []

def Predict(user1,item,nearest_neighbors):
    sum = 0
    n = len(movie_rated_user1)
    for user1_item in movie_rated_user1:
        sum += ratings_matrix[user1][user1_item]
    user1_avg = sum/n


    neighbor_rating_item = 0
    numerator = 0
    denominator = 0
    for candidate_neighbor in nearest_neighbors:
        nearest_sum = 0
        count = 0
        for movie,rating in ratings_matrix[candidate_neighbor[0]].iteritems():
            if movie <> item:
                nearest_sum += rating
                count += 1
            else:
                pass

        nearest_avg = nearest_sum/count
        numerator += (ratings_matrix[candidate_neighbor[0]][item] - nearest_avg) * candidate_neighbor[1]
        denominator += abs(candidate_neighbor[1])

    similarity = user1_avg + numerator/denominator
    return similarity

def pearson_correlation(user1,user2):
    movie_rated_candidate = []
    co_rated_items = []
    for movie, rating in ratings_matrix[user2].iteritems():
        movie_rated_candidate.append(movie)
    co_rated_items = list(set(movie_rated_user1) & set(movie_rated_candidate))

    user1_sum = 0
    user2_sum = 0
    n = len(co_rated_items)

    # AVG CALCULATION
    for co_item in co_rated_items:
        user1_sum += ratings_matrix[user1][co_item]
        user2_sum += ratings_matrix[user2][co_item]

    user1_avg = user1_sum/n
    user2_avg = user2_sum/n

    # SIMILARITY
    numerator = 0
    denominator = 0
    denom_user1 = 0
    denom_user2 = 0
    for co_item in co_rated_items:
        numerator += (ratings_matrix[user1][co_item] - user1_avg) * (ratings_matrix[user2][co_item] - user2_avg)
        denom_user1 += math.pow(ratings_matrix[user1][co_item] - user1_avg,2)
        denom_user2 += math.pow(ratings_matrix[user2][co_item] - user2_avg,2)
    denominator = math.sqrt(denom_user1) * math.sqrt(denom_user2)

    similarity = numerator/denominator
    return user2,similarity

def K_nearest_neighbors(user1,k):

   nearest_neighbor = []
   for movie,rating in ratings_matrix[user1].iteritems():
       movie_rated_user1.append(movie)

   candidates = [K for K in ratings_matrix.keys()]
   candidates.remove(user1)

   for candidate_neighbor in candidates:
       user2,similarity = pearson_correlation(user1,candidate_neighbor)
       nearest_neighbor.append((user2,similarity))

   temp_list = sorted(nearest_neighbor, key=lambda element: (-element[1], element[0]))
   # add length check for k < n
   return temp_list


def main(argv):
    with open(argv[1], 'r') as tsv:
        user_id = argv[2]
        movie_to_rate = argv[3]
        k = int(argv[4])
        k_nearest_neighbors = []
        for line in tsv:
            each_rating = line.split("\t")
            if each_rating[0] not in ratings_matrix.keys():
                ratings_matrix[each_rating[0]] = {}
                ratings_matrix[each_rating[0].strip()][each_rating[2].strip()] = float(each_rating[1])
            else:
                ratings_matrix[each_rating[0].strip()][each_rating[2].strip()] = float(each_rating[1])


        neighbors = K_nearest_neighbors(user_id,k)
        c = 1
        for candidate_neighbor in neighbors:
            if movie_to_rate in ratings_matrix[candidate_neighbor[0]].keys() and c <= k:
                print candidate_neighbor[0] , candidate_neighbor[1]
                k_nearest_neighbors.append(candidate_neighbor)
                c += 1



        similarity = Predict(user_id,movie_to_rate,k_nearest_neighbors)
        print similarity


if __name__ == '__main__':
    main(sys.argv)