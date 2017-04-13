import sys
import os
import subprocess
import argparse
import shutil

sub_test_dirs = list()
ignore_tests = ['ISORC2017']

def get_directory_contents(parent_dir):
	for child in os.listdir(parent_dir):
		if child in ignore_tests:
			continue
		path = os.path.join(parent_dir, child)
		if os.path.isdir(path):
			if child == 'configs':
				zopkio_script = os.path.join(parent_dir, 'main_test.py')
				if os.path.exists(zopkio_script):
					#print("Parent Dir: \t" + parent_dir)
					#print("FOLDER: \t" + path)
					#print("Zopkio Script: \t" + zopkio_script)
					configs_jenkins = os.path.join(parent_dir, 'configs_jenkins', 'config.json')
					if os.path.exists(configs_jenkins):
						shutil.copy(configs_jenkins, path)
					sub_test_dirs.append(parent_dir)
					return
			else:
				get_directory_contents(path)


def main(test_dir, results_dir):
	#test_dir = os.path.join(test_dir, 'tests')

	if os.path.exists(test_dir):
		get_directory_contents(test_dir)

	test_to_result_dir_map = dict()
	base_path_length = len(test_dir)
	#print (sub_test_dirs)
	for i in sub_test_dirs:
		result_sub_dir = i[base_path_length:]
		result_sub_dir = results_dir + result_sub_dir

		try:
			if not os.path.exists(result_sub_dir):
				os.makedirs(result_sub_dir)

			call_zopkio(os.path.join(i, 'main_test.py'), result_sub_dir)
		except Exception as e:
			print (str(e))

def call_zopkio(test_script_path, log_dir):
	zopkio = '/usr/local/bin/zopkio'
	try:
		if os.path.exists(test_script_path):
			subprocess.call([zopkio, '--nopassword', test_script_path, '--output-dir', log_dir])
	except Exception as e:
		print (str(e))


if __name__ == "__main__":
    test_dir = None
    results_dir = None
    parser = argparse.ArgumentParser('Jenkins Zopkio Automation Script')
    parser.add_argument('-t', action='store', help='Test directory where zopkio tests are located.')
    parser.add_argument('-r', action='store', help='Results directory where logs will be.')

    try:
        args = parser.parse_args()
        if args.t is not None:
            test_dir = args.t
        if args.r is not None:
            results_dir = args.r

        if test_dir is not None and results_dir is not None:
			main(test_dir, results_dir)
    except Exception as e:
        print("Unexpected error: ", e)

