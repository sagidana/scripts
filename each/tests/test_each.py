import subprocess
import sys


def each(*argv, stdin=''):
    result = subprocess.run([sys.executable, '-m', 'each'] + list(argv),
                            input=stdin,
                            capture_output=True,
                            text=True)
    return result.returncode, result.stdout, result.stderr


def test_line_on_stdin_output_as_block():
    code, out, err = each('tr', 'a-z', 'A-Z', stdin='abc\n')
    assert code == 0
    assert out == 'abc\nABC\n\n'


def test_pipeline_stages():
    code, out, err = each('tr', 'a-z', 'A-Z', '|', 'rev', stdin='abc\n')
    assert out == 'abc\nCBA\n\n'


def test_blocks_in_input_order_when_parallel():
    script = 'import sys, time; line = sys.stdin.read(); time.sleep(0.3 / int(line)); print(line.strip())'
    code, out, err = each('-j', '3', sys.executable, '-c', script, stdin='1\n2\n3\n')
    assert out == '1\n1\n\n2\n2\n\n3\n3\n\n'


def test_words_are_passed_verbatim():
    script = 'import sys; print(sys.argv[1:])'
    code, out, err = each(sys.executable, '-c', script, 'two words', '*', '--', stdin='x\n')
    assert out == "x\n['two words', '*', '--']\n\n"


def test_empty_output_is_just_the_line():
    code, out, err = each('true', stdin='x\n')
    assert out == 'x\n\n'


def test_blank_input_lines_are_skipped():
    code, out, err = each('cat', stdin='\na\n  \nb\n')
    assert out == 'a\na\n\nb\nb\n\n'


def test_failed_job_sets_exit_status():
    code, out, err = each('false', stdin='a\n')
    assert code == 1
    assert out == 'a\n\n'


def test_failed_stage_in_the_middle_counts():
    code, out, err = each('false', '|', 'cat', stdin='a\n')
    assert code == 1


def test_missing_command():
    code, out, err = each('no-such-command-here', stdin='a\n')
    assert code == 1
    assert 'each: no-such-command-here:' in err


def test_no_command_is_a_usage_error():
    code, out, err = each(stdin='a\n')
    assert code == 2
    code, out, err = each('cat', '|', stdin='a\n')
    assert code == 2


def test_jobs_must_be_positive():
    code, out, err = each('-j', '0', 'cat', stdin='a\n')
    assert code == 2


def test_stderr_is_grouped_with_the_block_in_order():
    script = 'import sys, time; line = sys.stdin.read().strip(); time.sleep(0.3 / int(line)); sys.stderr.write("err " + line + "\\n"); print("out " + line)'
    code, out, err = each('-j', '3', sys.executable, '-c', script, stdin='1\n2\n3\n')
    assert out == '1\nout 1\n\n2\nout 2\n\n3\nout 3\n\n'
    assert err == 'err 1\nerr 2\nerr 3\n'


def test_stderr_of_every_stage_is_captured():
    code, out, err = each('sh', '-c', 'echo first >&2', '|', 'sh', '-c', 'cat; echo second >&2', stdin='a\n')
    assert out == 'a\n\n'
    assert sorted(err.splitlines()) == ['first', 'second']
