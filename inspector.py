#!/usr/bin/env python3
import argparse
import os
import math
import itertools
from pathlib import Path
import fcntl
import sys
import socket
import io
import contextlib
import shutil
import traceback
import pickle

from ruamel import yaml
from kerncraft import prefixedunit
from kerncraft import kerncraft
from stempel import stempel

import utils

__version__ = '2.0.dev0'
config = {
    'base_dirpath': Path('.')
}

# TODO:
# * Kernel code generation
# * Job(s) execution
# * Job submission
# * Job queue status gathering
# * Workload processing
# * Job requeuing

class Kernel:
    """Describes a kernel including sizes to model and execute for."""
    @classmethod
    def get_all(cls, filter_type, filter_parameter):
        with config['base_dirpath'].joinpath('config', 'kernels.yml').open() as f:
            kernel_dicts = yaml.load(f, Loader=yaml.Loader)
        for kd in kernel_dicts:
            if filter_type is not None and kd['type'] not in filter_type:
                continue
            if filter_parameter is not None and kd['parameter'] not in filter_parameter:
                continue
            yield cls(**kd)

    def __init__(self, type, parameter, scaling=None, steps=None):
        self.type = type
        self.parameter = parameter
        self.scaling = scaling
        self.steps = steps
        if scaling and steps is None:
            self.steps = generate_steps(**scaling)
        else:
            self.steps = []
    
    def get_code(self):
        if self.type == "named":
            with config['base_dirpath'].joinpath('kernels', self.parameter).open() as f:
                code = f.read()
        elif self.type == "stempel":
            codeio = io.StringIO()
            parser = stempel.create_parser()
            args= parser.parse_args(["foo", "bar", "TODO"])  # TODO
            stempel.run_gen(args, parser, output_file=codeio)
            code = codeio.getvalue()
            codeio.close()
        else:
            raise ValueError("Unsupported kernel type: {}".format(self.type))
        return code
    
    def save_to(self, path):
        """Save kernel code to path."""
        with path.open('w') as f:
            f.write(self.get_code())
    
    def __repr__(self):
        steps = self.steps
        if self.scaling:
            steps = self.scaling
        return "<Kernel {!r} {!r} {!r}>".format(self.type, self.parameter, steps)

class Host:
    """Describes a host on which kernels may be executed and modelled."""
    @classmethod
    def get_all(cls, filter_names=None):
        with config['base_dirpath'].joinpath('config', 'hosts.yml').open() as f:
            hosts_dict = yaml.load(f, Loader=yaml.Loader)
        for name, hd in hosts_dict.items():
            if filter_names is not None and name not in filter_names:
                continue
            try:
                yield cls(name=name, **hd)
            except TypeError:
                traceback.print_exc()
    
    def __init__(self, name, nodelist=[], submission_host=None, slurm_arguments='',
                 runtime_setup=[], machine_filename=None):
        self.name = name
        self.nodelist = nodelist
        self.submission_host = submission_host
        self.slurm_arguments = slurm_arguments
        self.runtime_setup = runtime_setup
        self.machine_filename = machine_filename
        # Load contents of machine file into machine_file
        if machine_filename is not None:
            with self.get_machine_filepath().open() as f:
                self.machine_file = yaml.load(f, Loader=yaml.Loader)
    
    def get_machine_filepath(self):
        return config['base_dirpath'].joinpath('machine_files', self.machine_filename)
    
    def enqueue_execution(self, cli_args):
        print("TODO enqueue on", self.name, ':', ' '.join(cli_args))
        # TODO eunqueue
        # * build job file string
        # * pass to slurm
    
    def get_queued_executions(self):
        """Return list of queued cli_args and status"""
        raise NotImplementedError

    def get_compilers(self):
        """Return list of compilers from host description."""
        return list(self.machine_file['compiler'].keys())
    
    def is_current_host(self):
        """Return True if executing host is mentioned in nodelist"""
        return socket.gethostname().split('.')[0] in self.nodelist


class Workload:
    """
    Describes the complete modelling, measurement and reporting of a single kernel on a single host.
    """
    @classmethod
    def get_all(cls, kernels, hosts):
        return [cls(k, h) for k, h in itertools.product(kernels, hosts)]

    def __init__(self, kernel, host):
        self.kernel = kernel
        self.host = host
    
    def get_wldir(self):
        """Initialize and return path to workload directory"""
        wldir = config['base_dirpath'].joinpath(
            'jobs', self.host.name, self.kernel.type, self.kernel.parameter)
        if not wldir.exists():
            wldir.mkdir(parents=True)
        
        # Save kernel file
        kernel_filename = wldir.joinpath('kernel.c')
        if not kernel_filename.exists():
            self.kernel.save_to(kernel_filename)
        
        # Copy machine file
        machine_filename = wldir.joinpath('machine.yml')
        if not machine_filename.exists():
            shutil.copy(str(self.host.get_machine_filepath()), str(machine_filename))
        return wldir

    def get_jobs(self, compiler=None, steps=None, incore_model=None, cores=None):
        if hasattr(self, '_jobs'):
            return self._jobs
        
        kc_base_args = [
            '-vvv',
            '-m', 'machine.yml',
            'kernel.c']
        # Layer Conditions
        jobs = [Job(self,
                    kc_base_args + ['-D', '.', '100', '-p', 'LC'],        
                    exec_on_host=False)]
        for s in self.kernel.steps:
            if steps is not None and s not in steps:
                continue
            kc_step_args = kc_base_args + ['-D', '.', str(s)]
            for cc in self.host.get_compilers():
                if compiler is not None and cc not in compiler:
                    continue
                kc_step_cc_args = kc_step_args + ['-C', cc]
                # Benchmark
                cores_per_socket = (self.host.machine_file['NUMA domains per socket'] 
                                    * self.host.machine_file['cores per NUMA domain'])
                for c in range(1, cores_per_socket + 1):
                    if cores is not None and c not in cores:
                        continue
                    # TODO Run 2-N cores at the same time?
                    jobs.append(Job(self,
                                    kc_step_cc_args + ['-p', 'Benchmark', '-c', str(c)],
                                    exec_on_host=True))
                for icm in self.host.machine_file['in-core model'].keys():
                    if incore_model is not None and icm not in incore_model:
                        continue
                    kc_step_cc_icm_args = kc_step_cc_args + ['-i', icm]
                    # ECM
                    # TODO split into ECMData and ECMCPU?
                    # TODO run ECMCPU only once
                    jobs.append(Job(self,
                                    kc_step_cc_icm_args + ['-p', 'ECM'],        
                                    exec_on_host=False))
                    # RooflineIACA
                    # TODO join with ECMCPU+ECMData?
                    jobs.append(Job(self,
                                    kc_step_cc_icm_args + ['-p', 'RooflineIACA'],        
                                    exec_on_host=False))
        self._jobs = jobs
        return jobs


    # TODO jobs status tracking functionality
    # TODO report generation function


class Job:
    """
    A single job to be executed on a host by a single Kerncraft run.
    
    Can be used to execute a new or unfished job or to collect resulting data
    and detect state (i.e., new, executing, finished or failed).
    """
    def __init__(self, workload, kerncraft_args, exec_on_host):
        """
        Construct Job object.
        
        :param kernel: kernel to analyze
        :param host: host this job is running for
        :param kerncraft_args: list of cli arguments to pass to kerncraft (including machine file)
        :param exec_on_host: if True, execute this job only on specified host, otherwise use any
        """
        self.workload = workload
        self.kernel = workload.kernel
        self.host = workload.host
        self.kerncraft_args = kerncraft_args
        self.exec_on_host = exec_on_host

        self._have_lock = False
        self._lockfile_path = self.get_jobdir().with_suffix('.lock')
        self._lock_fd = None

        self._state = self.get_state()
    
    def __repr__(self):
        return "<Job {} {!r} {} {}>".format(
            self.host.name, self.kernel, self.kerncraft_args, self.exec_on_host)
    
    def check_hostname(self):
        return socket.gethostname().split('.')[0] in self.host.nodelist
    
    def _aquire_lock(self, non_blocking=False):
        """Lock job directory"""
        if self._have_lock:
            return True
        self._lock_fd = self._lockfile_path.open('w')
        operation = fcntl.LOCK_EX
        if non_blocking:
            operation |= fcntl.LOCK_NB
        try:
            fcntl.flock(self._lock_fd, operation)
        except IOError:
            return False
        self._have_lock = True
        return True
    
    def is_locked(self):
        # May be locked, but good enough
        return self._lockfile_path.exists()
    
    def _release_lock(self):
        if not self._have_lock:
            return
        fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
        self._lockfile_path.unlink()
        self._lock_fd.close()
        self._lock_fd = None
    
    def get_jobdir(self):
        """Return job directory path."""
        return self.workload.get_wldir() / ' '.join(self.kerncraft_args).replace('/', '$')

    def execute(self, non_blocking=False):
        """Change state from new or enqueud to executing."""
        if self._state in ['finished', 'failed']:
            return
        assert not self.exec_on_host or self.check_hostname(), \
            "Needs to run on specified host: "+repr(self.host)
        self.get_jobdir().mkdir(parents=True, exist_ok=True)
        self._aquire_lock(non_blocking=non_blocking)
        self._state = "executing"

        #import pdb; pdb.set_trace()

        # Execute kerncraft workload
        # TODO place Kerncraft specific code in seperate function make subclass
        try:
            parser = kerncraft.create_parser()
            with chdir(str(self.workload.get_wldir())):
                args = parser.parse_args(self.kerncraft_args)
                kerncraft.check_arguments(args, parser)
                with open(self.get_jobdir().joinpath('out.txt'), 'w') as f:
                    with utils.stdout_redirected(to=sys.stdout, stdout=sys.stderr):
                        with utils.stdout_redirected(f):
                            result_storage = kerncraft.run(parser, args)
                with open(self.get_jobdir().joinpath('out.pickle'), 'wb') as f:
                    pickle.dump(result_storage, f, protocol=4)
            failed = False
        except KeyboardInterrupt:
            failed = True
            # Rollback by removing jobdir
            shutil.rmtree(str(self.get_jobdir()))
            print("Manual abort. Cleared currently running job data.")
            sys.exit(1)
        except:
            failed = True
            traceback.print_exc(file=sys.stderr)
            print("Kerncraft run failed.", file=sys.stderr)
        finally:
            if not failed:
                self._state = "finished"
                try:
                    with self.get_jobdir().joinpath('FINISHED').open('w') as f:
                        f.write(self._state)
                except IOError as e:
                    print("Could not write FINISHED file:", e, file=sys.stderr)
            else:
                self._state = "failed"
                # Nothing needs to be stored
                # directory exists && no lock && no FINISHED file in combination mean failed
            self._release_lock()
    
    def get_state(self):
        """Indicate if this job is new, executing, finished or failed."""
        self._state = "new"
        if self.get_jobdir().is_dir():
            if self.is_locked():
                self._state = "executing"
            else:
                if self.get_jobdir().joinpath('FINISHED').exists():
                    self._state = 'finished'
                else:
                    self._state = 'failed'
        return self._state

    def get_outputs(self):
        assert self._state == 'finished', "Can only be run on sucessfully finished jobs."
        # TODO
        raise NotImplementedError


class VersionAction(argparse.Action):
    """Reimplementation of the version action, because argparse's version outputs to stderr."""
    def __init__(self, option_strings, version, dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help="show program's version number and exit"):
        super(VersionAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)
        self.version = version

    def __call__(self, parser, namespace, values, option_string=None):
        print(parser.prog, self.version)
        parser.exit()


def enqueue(type=None, parameter=None, machine=None, compiler=None, steps=None, 
            incore_model=None, cores=None, **kwargs):
    hosts = list(Host.get_all(filter_names=machine))
    kernels = list(Kernel.get_all(filter_type=type, filter_parameter=parameter))
    workloads = []
    jobs = []
    for h in hosts:
        wls = list(Workload.get_all(kernels, [h]))
        workloads.extend(wls)
        # Build list of jobs by chaining workload job lists
        if any([w.get_jobs(
                    compiler=compiler, steps=steps, incore_model=incore_model, cores=cores
                ) for w in wls]):
            # Queue this filterset for execution on host
            h.enqueue_execution(make_cli_args(
                type=type, parameter=parameter, machine=machine, compiler=compiler, steps=steps, 
                incore_model=incore_model, cores=incore_model))

    # Just FYI
    print(len(hosts), "hosts")
    print(len(kernels), "kernels")
    print(len(workloads), "workloads")


def status(type=None, parameter=None, machine=None, compiler=None, steps=None, 
           incore_model=None, cores=None, **kwargs):
    raise NotImplementedError


def execute(type=None, parameter=None, machine=None, compiler=None, steps=None, 
            incore_model=None, cores=None, **kwargs):
    hosts = list(Host.get_all(filter_names=machine))
    kernels = list(Kernel.get_all(filter_type=type, filter_parameter=parameter))
    workloads = []
    jobs = []
    wls = list(Workload.get_all(kernels, hosts))
    workloads.extend(wls)
    # Build list of jobs by chaining workload job lists
    jobs = list(itertools.chain(*[w.get_jobs(
                compiler=compiler, steps=steps, incore_model=incore_model, cores=cores
            ) for w in wls]))
    # Filter jobs which do not match current host but require this
    jobs = [j for j in jobs if not j.exec_on_host or j.check_hostname()]
    
    # Just FYI
    print(len(hosts), "hosts")
    print(len(kernels), "kernels")
    print(len(workloads), "workloads")
    print(len(jobs), "jobs")


    for j in jobs:
        print(j.get_state(), j)
        j.execute()


def process(type=None, parameter=None, machine=None, **kwargs):
    raise NotImplementedError


def upload(type=None, parameter=None, machine=None, **kwargs):
    raise NotImplementedError


def get_args(args=None):
    """Return parsed commandline arguments."""
    if hasattr(get_args, '_parsed_args'):
        return get_args._parsed_args

    parser = argparse.ArgumentParser(description='INSPECT Command Line Utility')
    parser.add_argument('--version', action=VersionAction, version='{}'.format(__version__))
    parser.add_argument('--base-dir', '-b', type=Path, default=Path('.'),
                        help='Base directory to use for config and intermediate files.')

    # Workload filter:
    parser.add_argument('--type', '-t', action='append',
                        help='Kernel type(s) to consider')
    parser.add_argument('--parameter', '-p', action='append',
                        help='Kernel parameter(s) to consider')
    parser.add_argument('--machine', '-m', action='append',
                        help='Machine name(s) to consider')

    # Jobs filter:
    parser.add_argument('--compiler', '-C', action='append',
                        help='Compiler(s) to consider')
    parser.add_argument('--steps', '-s', type=int, action='append',
                        help='Step(s) to consider')
    parser.add_argument('--incore-model', '-i', action='append',
                        help='In-core model(s) to consider')
    parser.add_argument('--cores', '-c', type=int, action='append',
                        help='Core count(s) to consider')

    subparsers = parser.add_subparsers(
        title='command', dest='command', description='action to take', help='Valid commands:')
    subparsers.required = True
    
    # enqueue: workload + jobs
    enqueue_parser = subparsers.add_parser('enqueue', help='Generate and enqueue jobs')
    enqueue_parser.set_defaults(action_function=enqueue)
    # status: workload + jobs
    status_parser = subparsers.add_parser('status', help='Check status of jobs')
    status_parser.set_defaults(action_function=status)
    # execute: workload + jobs
    execute_parser = subparsers.add_parser(
        'execute', help='Execute suitable jobs and collect raw outputs')
    execute_parser.set_defaults(action_function=execute)
    # process: workload
    process_parser = subparsers.add_parser(
        'process', help='Process workload reports from raw job outputs')
    process_parser.set_defaults(action_function=process)
    # uload: workload
    upload_parser = subparsers.add_parser(
        'upload', help='Upload and combine workload reports into website')
    upload_parser.set_defaults(action_function=upload)
    get_args._parsed_args = parser.parse_args(args=args)
    get_args._parsed_args.base_dir = get_args._parsed_args.base_dir.absolute()
    return get_args._parsed_args


def make_cli_args(ignore_list=['command', 'action_function'], **kwargs):
    """
    Turn Namespace into args list passable to get_args.
    
    Quite dumb, will only work with default naming scheme.
    """
    args = []
    for key, value in kwargs.items():
        if value is None: continue
        if key in ignore_list: continue
        argument = '--' + key.replace('_', '-')
        if type(value) is list:
            for item in value:
                args += [argument, str(item)]
        else:
            args += [argument, str(value)]
    return args


def generate_steps(
    first, last, steps=100, stepping='log', multiple_of=8, no_powers_of_two=True):
    """
    Generate a list of sizes, based on scaling dictionary description.

    :param first: first element in resuliting list
    :param last: last element in resulting list
    :param steps: total number of elements in resulting list
    :param stepping: use linear ('lin') or logarithmic ('log') stepping
    :param multiple_of: force all sizes to be a multiple of this
    :param no_powers_of_two: check for powers of two and avoid those

    Length of returned list is not guaranteed.
    """
    results = [first]

    if stepping not in ['log', 'lin']:
        raise ValueError("Unknown stepping parameter. Use 'lin' or 'log'.")

    intermediate = first
    while len(results) < steps and intermediate < last:
        if stepping == 'log':
            stepwidth = (math.log10(last) - math.log10(intermediate))/(steps-len(results))
            intermediate = 10**(math.log10(intermediate) + stepwidth)
        else:
            stepwidth = (last - intermediate)/(steps-len(results))
            intermediate += stepwidth

        intermediate = round(intermediate)
        while True:
            if multiple_of is not None:
                if intermediate % multiple_of != 0:
                    # Increase to next multiple of
                    intermediate += multiple_of - intermediate % multiple_of
                    continue
            if no_powers_of_two:
                if intermediate != 0 and ((intermediate & (intermediate - 1)) == 0):
                    intermediate += 1
                    continue
            if results[-1] == intermediate:
                # Do not insert same element twice
                intermediate += 1
                continue
                
            results.append(intermediate)
            break
    if results[-1] < last:
        results.append(last)
    return results


@contextlib.contextmanager
def chdir(pathstr):
    old_cwd = os.getcwd()
    try:
        os.chdir(pathstr)
        yield
    finally:
        os.chdir(old_cwd)


def main():
    args = get_args()
    global base_dirpth
    config['base_dirpath'] = args.base_dir
    args.action_function(**vars(args))


if __name__ == '__main__':
    main()