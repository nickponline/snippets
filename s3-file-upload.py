import os
import sys
 
from boto.s3.connection import S3Connection
from boto.s3.key import Key


for index, infile in enumerate(sys.argv[1:]):
	local_file_path = infile
	
	conn = S3Connection('AKIAJ7VIDNPJTDBUWC7Q', 'DSovWhtg9WygOd85Ip4nPAwGBHKnyTNRFyHxKJHv')
	pb = conn.get_bucket('denoise.slice.all')

	k = Key(pb)
	file_name_to_use_in_s3 = os.path.basename(local_file_path)
	k.name = file_name_to_use_in_s3
	k.set_contents_from_filename(local_file_path)

	print index, len(sys.argv[1:])