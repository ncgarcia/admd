# https://gist.github.com/batzner/7c24802dd9c5e15870b4b56e22135c96
import sys
import getopt
import tensorflow as tf
# import ipdb

usage_str = 'python codebase_rename_ckpt.py --checkpoint_dir=path/to/dir/ --checkpoint_new=path/to/dir/  --replace_from=substr --replace_to=substr --add_prefix=abc --dry_run'


def rename(checkpoint_dir, checkpoint_new, replace_from, replace_to, add_prefix, dry_run):
    # checkpoint = tf.train.get_checkpoint_state(checkpoint_dir)
    tf_config = tf.ConfigProto(log_device_placement=True)

    with tf.Session(config=tf_config) as sess:
        # ipdb.set_trace()
        with tf.device('/cpu:0'):
            for var_name, _ in tf.contrib.framework.list_variables(checkpoint_dir):
                # Load the variable
                var = tf.contrib.framework.load_variable(
                    checkpoint_dir, var_name)

                # Set the new name
                new_name = var_name
                if None not in [replace_from, replace_to]:
                    new_name = new_name.replace(replace_from, replace_to)
                if add_prefix:
                    new_name = add_prefix + new_name

                if dry_run:
                    print('%s would be renamed to %s.' % (var_name, new_name))
                else:
                    print('Renaming %s to %s.' % (var_name, new_name))
                    # Rename the variable
                    var = tf.Variable(var, name=new_name)

            if not dry_run:
                # Save the variables
                saver = tf.train.Saver()
                sess.run(tf.global_variables_initializer())
                if not checkpoint_new:
                    saver.save(sess, checkpoint_dir)
                else:
                    saver.save(sess, checkpoint_new)


def main(argv):
    checkpoint_dir = None
    checkpoint_new = None
    replace_from = None
    replace_to = None
    add_prefix = None
    dry_run = False

    try:
        opts, args = getopt.getopt(argv, 'h', ['help=', 'checkpoint_dir=', 'checkpoint_new=', 'replace_from=',
                                               'replace_to=', 'add_prefix=', 'dry_run'])
    except getopt.GetoptError:
        print(usage_str)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage_str)
            sys.exit()
        elif opt == '--checkpoint_dir':
            checkpoint_dir = arg
        elif opt == '--checkpoint_new':
            checkpoint_new = arg
        elif opt == '--replace_from':
            replace_from = arg
        elif opt == '--replace_to':
            replace_to = arg
        elif opt == '--add_prefix':
            add_prefix = arg
        elif opt == '--dry_run':
            dry_run = True

    if not checkpoint_dir:
        print('Please specify a checkpoint_dir. Usage:')
        print(usage_str)
        sys.exit(2)

    rename(checkpoint_dir, checkpoint_new, replace_from,
           replace_to, add_prefix, dry_run)


if __name__ == '__main__':
    main(sys.argv[1:])
