#! /usr/bin/python

## @file
# This file is part of scons-tools.
#
# @author Sebastian Rettenberger <sebastian.rettenberger@tum.de>
#
# @copyright Copyright (c) 2016-2017, Technische Universitaet Muenchen.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import utils.checks
import utils.pkgconfig

def find(env, required=True, parallel=False):
	conf = env.Configure()
	utils.checks.addDefaultTests(conf)

	flags = False
	if parallel:
		# Required for parallel netcdf on some cray machines
		flags = utils.pkgconfig.parse(conf, 'netcdf_parallel')
	if not flags:
		flags = utils.pkgconfig.parse(conf, 'netcdf')
	if not flags:
		if required:
			utils.checks.error('Could not find netcdf with pkg-config: Make sure pkg-config is installed and PKG_CONFIG_PATH contains netcdf.pc')
			env.Exit(1)
		else:
			conf.Finish()
			return False

	utils.pkgconfig.appendPathes(env, flags)

	if parallel:
		header = 'netcdf_par.h'
	else:
		header = 'netcdf.h'

	if not conf.CheckLibWithHeader(flags['LIBS'][0], header, 'c', extra_libs=flags['LIBS'][1:]):
		if required:
			utils.checks.error('Could not find netCDF')
			env.Exit(1)
		else:
			conf.Finish()
			return False

	conf.Finish()
	return True
