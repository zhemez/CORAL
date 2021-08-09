__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2021, National Renewable Energy Laboratory"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.nunemaker@nrel.gov"


import os

import yaml
from simpy import Resource
from ORBIT.core.library import loader


class SharedLibrary:
    """Class used to model shared library resources for ORBIT simulations."""

    def __init__(self, env, path, allocations):
        """
        Creates an instance of `SharedLibrary`.

        Parameters
        ----------
        path : str
            Path to library items.
        allocations : dict
            Number of each library item that exists in the shared environment.
        """

        self.env = env
        self._path = path
        self._alloc = allocations
        self._resources = {}

        self.initialize_shared_resources()

    @property
    def resources(self):
        """Return dictionary of shared resource sets."""

        return self._resources

    def initialize_shared_resources(self):
        """Initializes shared resources in `self._alloc`."""

        for cat_name, cat_items in self._alloc.items():
            for key, (name, cap) in cat_items.items():

                path = os.path.join(self._path, cat_name, f"{name}.yaml")
                resource = SharedResourceSet(self.env, path, cap)
                self._resources[key] = resource


class SharedResourceSet:
    """Class to represent a shared set of resources."""

    def __init__(self, env, path, capacity):
        """
        Creates an instance of `SharedResourceSet`.

        Parameters
        ----------
        env : Environment
            Environment where shared resources are held.
        path : str
            Path to library item
        capacity : int
            Number of resources in the shared resource set.
        """

        self.env = env
        self.path = path
        self.capacity = capacity

        self.load_data()
        self.initialize_router()

    def load_data(self):
        """Load library data for eventual insert into ORBIT config."""

        with open(self.path, "r") as f:
            data = yaml.load(f, Loader=loader)

        self.data = data

    def initialize_router(self):
        """Initialize resource router."""

        self.router = Resource(self.env, self.capacity)
