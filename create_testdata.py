pattern = f"*S*E*.mp4"

for file in Path('../The Man in the High Castle').glob(pattern):

     print(f"file: {file}")
     print(f"file.name: {file.name}")
     Path('.',file.name).touch()
