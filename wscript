import Options, Utils, sys
from os import unlink, symlink, popen
from os.path import exists, islink

srcdir = '.'
blddir = 'build'
VERSION = '0.0.7'

def set_options(ctx):
    ctx.tool_options('compiler_cxx')

def configure(ctx):
    ctx.check_tool('compiler_cxx')
    ctx.check_tool('node_addon')
    if sys.platform.startswith("sunos") or sys.platform.startswith("darwin"):
        ctx.env.append_value('CXXFLAGS', ['-D_HAVE_DTRACE'])

def build(ctx):
    if sys.platform.startswith("sunos") or sys.platform.startswith("darwin"):
        t = ctx.new_task_gen('cxx', 'shlib', 'node_addon')
        t.target = 'DTraceProviderBindings'
        t.source = ['dtrace_provider.cc', 'dtrace_dof.cc']
        if sys.platform.startswith("sunos"):
            t.source.append('solaris-i386/dtrace_probe.cc')
        elif sys.platform.startswith("darwin"):
            t.source.append('darwin-x86_64/dtrace_probe.cc')

def shutdown():
    t = 'DTraceProviderBindings.node'
    if Options.commands['clean']:
       if exists(t): unlink(t)
    if Options.commands['build']:
       if exists('build/default/' + t) and not exists(t):
          symlink('build/default/' + t, t)
       if exists('build/Release/' + t) and not exists(t):
          symlink('build/Release/' + t, t)
