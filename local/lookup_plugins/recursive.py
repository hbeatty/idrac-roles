# I didn't write this lookup plugin.
#
# Here is where I found it: https://gist.github.com/hkariti/d07695b4b9c5a68d8c02

import ansible.errors as errors
import ansible.utils as utils
 
class LookupModule(object):
    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir
 
    def lookup(self, name, args, inject):
        lookup = utils.lookup_loader.get(name)
        lookup.__init__(basedir=self.basedir)
        args = utils.template.template(self.basedir, args, inject, fail_on_undefined=True)
        return lookup.run(args, inject)
 
    def recursive_lookup(self, terms, previous_results, inject, all_items=[]):
        if not terms:
            return []
 
        current_term = terms[0]
        if not isinstance(current_term, dict) or 'name' not in current_term or 'args' not in current_term:
            raise AnsibleError("all args must contain 'name' and 'args' keys")
 
        all_items = all_items[:]
        results = []
        item_index = len(all_items)
        all_items.append(None)
        for r in previous_results:
            all_items[-1] = r
            inject['item'] = r
            inject['items'] = all_items
            inject['item_idx'] = item_index
            current_results = self.lookup(current_term['name'], current_term['args'], inject)
 
            if len(terms) > 1:
                results += self.recursive_lookup(terms[1:], current_results, inject, all_items)
            else:
                results += current_results
        return results
 
    def run(self, terms, inject=None, **kwargs):
        terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)
        if not isinstance(terms, (list, set)):
            raise errors.AnsibleError("expected list or set")
 
        initial_results = [None]
        return self.recursive_lookup(terms, initial_results, inject.copy())

