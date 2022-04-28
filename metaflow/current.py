from collections import namedtuple
import os

Parallel = namedtuple("Parallel", ["main_ip", "num_nodes", "node_index"])


class Current(object):
    def __init__(self):
        self._flow_name = None
        self._run_id = None
        self._step_name = None
        self._task_id = None
        self._retry_count = None
        self._origin_run_id = None
        self._namespace = None
        self._username = None
        self._is_running = False
        self._tags = None
        self._runtime_environment = None
        self._runtime_name = None
        self._sfn_state_machine_name = None
        self._max_workers = None
        self._max_num_splits = None

        def _raise(ex):
            raise ex

        self.__class__.graph = property(
            fget=lambda _: _raise(RuntimeError("Graph is not available"))
        )

    def _set_env(
        self,
        flow=None,
        run_id=None,
        step_name=None,
        task_id=None,
        retry_count=None,
        origin_run_id=None,
        namespace=None,
        username=None,
        is_running=True,
        tags=None,
    ):
        if flow is not None:
            self._flow_name = flow.name
            self.__class__.graph = property(fget=lambda _, flow=flow: flow._graph_info)

        self._run_id = run_id
        self._step_name = step_name
        self._task_id = task_id
        self._retry_count = retry_count
        self._origin_run_id = origin_run_id
        self._namespace = namespace
        self._username = username
        self._is_running = is_running
        self._tags = tags

        # from environment variables
        self._runtime_environment = os.environ.get(
            "METAFLOW_RUNTIME_ENVIRONMENT", "local"
        )
        self._runtime_name = os.environ.get("METAFLOW_RUNTIME_NAME", None)
        self._sfn_state_machine_name = os.environ.get("SFN_STATE_MACHINE", None)
        self._max_workers = os.environ.get("MAX_WORKERS", None)
        self._max_num_splits = os.environ.get("MAX_NUM_SPLITS", None)

    def _update_env(self, env):
        for k, v in env.items():
            setattr(self.__class__, k, property(fget=lambda _, v=v: v))

    def __contains__(self, key):
        return getattr(self, key, None) is not None

    def get(self, key, default=None):
        return getattr(self, key, default)

    @property
    def is_running_flow(self):
        return self._is_running

    @property
    def flow_name(self):
        return self._flow_name

    @property
    def run_id(self):
        return self._run_id

    @property
    def step_name(self):
        return self._step_name

    @property
    def task_id(self):
        return self._task_id

    @property
    def retry_count(self):
        return self._retry_count

    @property
    def origin_run_id(self):
        return self._origin_run_id

    @property
    def pathspec(self):
        return "/".join((self._flow_name, self._run_id, self._step_name, self._task_id))

    @property
    def namespace(self):
        return self._namespace

    @property
    def username(self):
        return self._username

    @property
    def parallel(self):
        return Parallel(
            main_ip=os.environ.get("MF_PARALLEL_MAIN_IP", "127.0.0.1"),
            num_nodes=int(os.environ.get("MF_PARALLEL_NUM_NODES", "1")),
            node_index=int(os.environ.get("MF_PARALLEL_NODE_INDEX", "0")),
        )

    @property
    def tags(self):
        return self._tags

    @property
    def runtime_environment(self):
        return self._runtime_environment

    @property
    def runtime_name(self):
        return self._runtime_name

    @property
    def sfn_state_machine_name(self):
        return self._sfn_state_machine_name

    @property
    def max_workers(self):
        return int(self._max_workers)

    @property
    def max_num_splits(self):
        return int(self._max_num_splits)


# instantiate the Current singleton. This will be populated
# by task.MetaflowTask before a task is executed.
current = Current()
