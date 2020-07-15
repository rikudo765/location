import uuid
import random
from colorama import Fore
from timeit import default_timer as timer
import sys
from app.main import loc_types, searcher, storage

sys.path.append('..')


class PerfLocation:
    def __init__(self):
        self.storage = storage.Storage()
        self.seed_id = "test-perf-loc-{}".format(uuid.uuid4())
        self.center = (81.14748070499664, 59.15039062500001)
        self.radius = 10
        self.in_region_cnt = 20
        self.out_region_cnt = 30

    def _add_point(self, pid, lat, long):
        self.storage.set_point(loc_types.Point(pid, lat, long))

    def _remove_point(self, pid):
        self.storage.remove_point(pid)

    def _search(self, latitude, longitude, radius, points_list):
        res = searcher.Search.search_points(latitude, longitude, radius, points_list)
        return res

    def _rand_point_in_region(self):
        lat = self.center[0]
        long = self.center[1]
        out = (lat + random.randint(1, 99) / 100, long + random.randint(1, 99) / 100)
        return out

    def _rand_point_out_region(self):
        lat = self.center[0]
        long = self.center[1]
        out = (lat + 30 + random.randint(1, 99) / 100, long + 30 + random.randint(1, 99) / 100)
        return out

    def perf_location_search(self):
        # generate in-region
        print(Fore.GREEN + "Generate in region points: {}".format(self.in_region_cnt))
        start = timer()
        for i in range(self.in_region_cnt):
            pid = "{}-{}".format(self.seed_id, i)
            p = self._rand_point_in_region()
            self._add_point(pid, p[0], p[1])

        print(Fore.GREEN + "Add time for {} points: {} (in seconds)".format(self.in_region_cnt, timer() - start))
        print("Done")

        # generate out of region
        start = timer()
        print(Fore.GREEN + "Generate out of region points: {}".format(self.out_region_cnt))
        for j in range(i + 1, self.out_region_cnt + self.in_region_cnt):
            pid = "{}-{}".format(self.seed_id, j)
            p = self._rand_point_out_region()
            self._add_point(pid, p[0], p[1])

        print(Fore.GREEN + "Add time for {} points: {} (in seconds)".format(self.out_region_cnt, timer() - start))
        print("Done")

        print(Fore.GREEN + "Search....")
        start = timer()
        prefix = searcher.Search.general_prefix(self.center[0], self.center[1], 100)
        res = self._search(self.center[0], self.center[1], 100, self.storage.get_points_by_pref(prefix))
        end = timer()

        print(Fore.GREEN + "Search time: {} (in seconds)".format(end - start))

        # is search valid?
        if len(res) == self.in_region_cnt:
            print(Fore.GREEN + "Search is valid")
        else:
            print(Fore.RED + "Search returned invalid result")

        # remove generated
        print(Fore.GREEN + "Remove test points...")
        for i in range(self.out_region_cnt + self.in_region_cnt):
            pid = "{}-{}".format(self.seed_id, i)
            self._remove_point(pid)

        print(Fore.GREEN + "Done")


if __name__ == '__main__':
    lp = PerfLocation()
    lp.perf_location_search()
