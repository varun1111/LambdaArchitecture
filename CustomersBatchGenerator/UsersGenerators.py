import subprocess
import ConfigParser

def run_cmd(args_list):
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    (output, errors) = proc.communicate()
    if proc.returncode:
        raise RuntimeError(
            'Error running command: %s. Return code: %d, Error: %s' % (
                ' '.join(args_list), proc.returncode, errors))
    return (output, errors)


if __name__=='__main__':
    config = ConfigParser.RawConfigParser()
    config.read('configFile.properties')
    userInputFile = config.get('UsersGenerator', 'USER_FILE')
    outputUsersHDFSPath = config.get('UsersGenerator', 'HDFS_LOCATION')
    (out, errors) = run_cmd(['hdfs', 'dfs', '-put', userInputFile, outputUsersHDFSPath])