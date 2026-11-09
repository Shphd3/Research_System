import sys,runpy
import transformers.utils.import_utils as iu
iu._torchvision_available=False
iu.is_flash_attn_2_available=lambda:False
import transformers.utils as u
u.is_flash_attn_2_available=lambda:False
path=sys.argv.pop(1)
runpy.run_path(path,run_name="__main__")
