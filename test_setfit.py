import os
import transformers
if not hasattr(transformers, 'training_args'):
    import transformers.training_args
if not hasattr(transformers.training_args, 'default_logdir'):
    def default_logdir(): pass
    transformers.training_args.default_logdir = default_logdir

from setfit import SetFitModel
print("SUCCESS")
