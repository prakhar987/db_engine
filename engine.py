import sqlparse
import os
import csv

class Table(object):
	#"""This is the class which holds the tables as objects and their lists """
    def __init__(self):
        self.name =""   ## Name of the table
        self.attributes=[] ## Attributes Name list
        self.box=""      ## 2-D tables

def convert_name_to_index(table_name):
	table_name=str(table_name)
	for i in range(len(table_list)):
		if(table_list[i].name==table_name):
			return i
	return -1
			
def setup_tables(loc):
	### Getting the Files first
	file_names="" ## will stroe the names of the files

	try:
		file_names=os.listdir(loc)
		print ("These files are found to build DB : ")
		for i in range(len(file_names)):
			print(file_names[i])

	except FileNotFoundError :
		print("Invalid location for DB files:",loc)
		print("Please try again")
		return 



	## Find schema files and build the tables 

	if "metadata.txt" not in file_names:
		print ("Schema (metadata.txt) absent")
		return 

	else:
		try:
			loc_meta=loc+'/metadata.txt'
			schema=[]
			with open(loc_meta,'r') as f:
				reader = f.read().splitlines()
				schema=reader

		except:
			print (e.message)
			return 

	## Now processing schema list
	table_list=[] ## Array that has all Table objects
	x=0
	i=0
	while(i<len(schema)):

		if(str(schema[i])=='<begin_table>'):
			new_obj=Table()
			table_list.append(new_obj)
			table_list[x].name=schema[i+1]
			i+=2
			continue
		if(str(schema[i])=='<end_table>'):
			x+=1
			i+=1
			continue
		table_list[x].attributes.append(str(schema[i]))
		i+=1


	# Now generating tables. Fill the data values
	for name in file_names:
				
				if(name !='metadata.txt' and name!='engine.py' and name!='.git'):
					loc_file=loc+'/'+name
					with open(loc_file,'r') as f:
						t_name = name.split('.')[0]
						## Now search in Table Objects
						for i in range(len(table_list)):
							if(table_list[i].name==str(t_name)):
								break
						## Now we add the table at correct postion in table_list
						read_table = [row for row in csv.reader(f, delimiter=',',skipinitialspace=True)]
						table_list[i].box=read_table
	


	print (".......Loading data values complete.\n")
	return table_list

def normal(first_box,second_box,box1_column,box2_column,flag,no_of_box):
	## Print Attribute Names
	for i in range(len(box1_column)):
		print(table_list[first_box].attributes[box1_column[i]],end="  ")
	if(no_of_box==2):
		for i in range(len(box2_column)):
			print(table_list[second_box].attributes[box2_column[i]],end="  ")
	print()


	for i in range(len(table_list[first_box].box)):
		tupel1=table_list[first_box].box[i]
		if(no_of_box==2) :  ## we have two tables
			for j in range(len(table_list[second_box].box)):
				tupel2=table_list[second_box].box[j]
				## we have two tuplels to print 
				for k in range(len(box1_column)):
					indx=box1_column[k]
					print(tupel1[indx],end=" ")
				for k in range(len(box2_column)):
					indx=box2_column[k]
					print(tupel2[indx],end=" ")
				print()

		else :
			for k in range(len(box1_column)):
					indx=box1_column[k]
					print(tupel1[indx],end=" ")
			print()

def agg(first_box,second_box,zz,flag,no_of_box,func_type):

	target=[]
	for i in range(len(table_list[first_box].box)):
		tupel=table_list[first_box].box[i]
		target.append(tupel[zz])

	sm=0
	for i in range (len (target)):
		target[i]=int(target[i])
		sm=sm+target[i]

	if(func_type==1): # max
			print("Max=",max(target))
	if(func_type==2): # min
			print("Min=",min(target))
	if(func_type==3): # avg
			sm=sm/len(target)
			print("Avg=",sm)
	if(func_type==4): # sum
		print("Sum=",sm)


def distinct(first_box,dist_col,flag,no_of_box):
	for i in range(len(dist_col)):
		print(table_list[first_box].attributes[dist_col[i]],end="  ")
	print()
	
	target=[]
	for i in range(len(table_list[first_box].box)):
		tupel=table_list[first_box].box[i]
		target.append(tupel[dist_col[0]])

	for i in range (len(target)):
		fg=0
		for j in range (i+1,len(target)):
			if(target[i]==target[j]):
				fg=1
				break
		if(fg==0):
			print(target[i])


def product(first_box,second_box,box1_column,box2_column,box1_lhs,box1_rhs,box2_lhs,box2_rhs,flag,no_of_box):
	for i in range(len(box1_column)):
		print(table_list[first_box].attributes[box1_column[i]],end="  ")
	if(no_of_box==2):
		for i in range(len(box2_column)):
			print(table_list[second_box].attributes[box2_column[i]],end="  ")
	print()

	if(no_of_box==2 or (no_of_box==1 and flag==0)):
	### And condition flag=3 , only one condition then flag=0
		if(flag==3 or flag==0 ) :
			for i in range(len(table_list[first_box].box)):
				tupel1=table_list[first_box].box[i]
				if(tupel1[box1_lhs]==box1_rhs):
					if(no_of_box==2) :  ## we have two tables
						for j in range(len(table_list[second_box].box)):
							tupel2=table_list[second_box].box[j]
							if(tupel2[box2_lhs]==box2_rhs):
								## we have two tuplels to print 
								for k in range(len(box1_column)):
									indx=box1_column[k]
									print(tupel1[indx],end=" ")
								for k in range(len(box2_column)):
									indx=box2_column[k]
									print(tupel2[indx],end=" ")
								print()
					else :

							 
								for k in range(len(box1_column)):
									indx=box1_column[k]
									print(tupel1[indx],end=" ")
								print() 

		if(flag==2)  : ## Or Condition
			for i in range(len(table_list[first_box].box)):
				tupel1=table_list[first_box].box[i]
			
				for j in range(len(table_list[second_box].box)):
					tupel2=table_list[second_box].box[j]

					if(tupel2[box2_lhs]==box2_rhs or tupel1[box1_lhs]==box1_rhs):
						## we have two tuplels to print 
						for k in range(len(box1_column)):
							indx=box1_column[k]
							print(tupel1[indx],end=" ")
						for k in range(len(box2_column)):
							indx=box2_column[k]
							print(tupel2[indx],end=" ")
						print()

	if(no_of_box==1 and (flag==2 or flag==3)): ### one box with two conditions
		for i in range(len(table_list[first_box].box)):
				tupel=table_list[first_box].box[i]

				if(flag==3): ## AND

			
							if(tupel[box2_lhs]==box2_rhs and tupel[box1_lhs]==box1_rhs):
								## we have two tuplels to print 
								for k in range(len(box1_column)):
									indx=box1_column[k]
									print(tupel[indx],end=" ")
								for k in range(len(box2_column)):
									indx=box2_column[k]
									print(tupel[indx],end=" ")
								print()

				if(flag==2): ## OR
							if(tupel[box2_lhs]==box2_rhs or tupel[box1_lhs]==box1_rhs):
								## we have two tuplels to print 
								for k in range(len(box1_column)):
									indx=box1_column[k]
									print(tupel[indx],end=" ")
								for k in range(len(box2_column)):
									indx=box2_column[k]
									print(tupel[indx],end=" ")
								print()




def join(first_box,second_box,box1_column,box2_column,box1_cond,box2_cond,flag,no_of_box):
	for i in range(len(box1_column)):
		print(table_list[first_box].attributes[box1_column[i]],end="  ")
	if(no_of_box==2):
		for i in range(len(box2_column)):
			print(table_list[second_box].attributes[box2_column[i]],end="  ")
	print()

	for i in range(len(table_list[first_box].box)):

		tupel1=table_list[first_box].box[i]

		for j in range(len(table_list[second_box].box)):
				tupel2=table_list[second_box].box[j]
				if(tupel1[box1_cond]==tupel2[box2_cond]):
					## we have two tuplels to print 
					for k in range(len(box1_column)):
						indx=box1_column[k]
						print(tupel1[indx],end=" ")
					for k in range(len(box2_column)):
						indx=box2_column[k]
						print(tupel2[indx],end=" ")
					print()
					
def resolve_function(): ## Tells if any Agg. function is present

	func=a[2]
	func_type=0
	if(func.find('max')>=0 or func.find('MAX')>=0):
		func_type=1
	if(func.find('min')>=0 or func.find('MIN')>=0):
		func_type=2
	if(func.find('avg')>=0 or func.find('AVG')>=0):
		func_type=3
	if(func.find('sum')>=0 or func.find('SUM')>=0):
		func_type=4
	return func_type

def resolve_distinct():
	dist=a[2]
	if(dist.find('distinct')>=0):
		return 1
		

def parser():

	first_box=""	## has index
	second_box=""	## has index
	box1_column=[] ## List of colms to print 
	box2_column=[] ## List of colms to print
	flag=1
	no_of_box=0

	## PARSE 'FROM'
	if(len(a)>=7 and len(a[6])!=0):		

		tmp = a[6]

		if "," not in tmp: ## Only one table
			tmp=tmp.strip()  ## extract name
			tmp=convert_name_to_index(tmp) ## convert to index
			if(tmp==-1):
				print("Table doesnt exist")
				return
			first_box=tmp  
			no_of_box=1

		else:
			table_names=tmp.split(',')
			tmp=table_names[0].strip()
			tmp=convert_name_to_index(tmp)
			if(tmp==-1):
				print("Table doesnt exist")
				return
			first_box=tmp

			tmp=table_names[1].strip()
			tmp=convert_name_to_index(tmp)
			if(tmp==-1):
				print("Table doesnt exist")
				return
			second_box=tmp
			no_of_box=2


	## If an aggregate function is present
	func_type=resolve_function()   
	if( func_type>0 and len(a)>=3 and len(a[2])!=0 ):

		tmp=a[2]
		for i in range(len(table_list[first_box].attributes)):
			z=tmp.find(table_list[first_box].attributes[i])
			if(z>=0):
				tmp=i
				if(len(a)==7):
					agg(first_box,second_box,tmp,flag,no_of_box,func_type)
					return


	## Handle Distinct keyword operations
	dist_flag=resolve_distinct()
	if(len(a)>=3 and len(a[2])!=0 and dist_flag==1):
		dist_col=[]
		tmp=a[2]
		for i in range(len(table_list[first_box].attributes)):
			z=tmp.find(table_list[first_box].attributes[i])
			if(z>=0):
				dist_col.append(i)
		distinct(first_box,dist_col,flag,no_of_box)
		return


							

	## PARSE  'SELECT'
	if(len(a)>=3 and len(a[2])!=0 ):		
				
		### Handle if Table is explicitly mentioned
		tmp=a[2]

		if ( '.' in tmp): ## eg Table1.A
				tmp = a[2]
				xyz=tmp.split(',')
				for i in range(len(xyz)):
					abc=xyz[i].split('.')
					table_extracted=abc[0].strip()
					## find index 
					table_extracted=convert_name_to_index(table_extracted)
					
					if(table_extracted==first_box):
						try:
							x=table_list[first_box].attributes.index(abc[1].strip()) 
						except ValueError :
							continue
						box1_column.append(x)
				
					
					if(table_extracted==second_box):
						try:
							x=table_list[second_box].attributes.index(abc[1].strip()) 
						except ValueError :
							continue
						box2_column.append(x)

						
		### Table not explicilty mentioned
		tmp=a[2]
		doesnt_exist=0
		if(	'.' not in tmp and a[2].strip() !='*') :
			col_select=tmp.split(',')
			for i in range(len(col_select)):
				col_select[i]=col_select[i].strip() ## Now col_select has all columns

			## Select Attributes to print from First Table
			tmp_lst=[] 			
			for i in range(len(col_select)):
				try:
					x=table_list[first_box].attributes.index(col_select[i]) ## Replace table1 with table to search
				except ValueError :
					doesnt_exist+=1
					continue
				tmp_lst.append(x)
				
			box1_column=tmp_lst  ## Converted Names to Indexes

			## Select Attributes to print from second Table
			if(no_of_box==2) :
				tmp_lst=[] 			
				for i in range(len(col_select)):
					try:
						x=table_list[second_box].attributes.index(col_select[i]) ## here also
					except ValueError:
						doesnt_exist+=1
						continue
					tmp_lst.append(x)
				box2_column=tmp_lst


		if(doesnt_exist==1 and no_of_box==1): ## works with only 1 table
			print("Wrong Attribute")
			doesnt_exist=0
			return

		### Handle '*'
		if '*' in a[2] :
			for i in range(len(table_list[first_box].attributes)): 
				box1_column.append(i)  ## only one box
			if(no_of_box==2):
				for i in range(len(table_list[second_box].attributes)): 
					box2_column.append(i)
		
		if(len(a)==7):
			normal(first_box,second_box,box1_column,box2_column,flag,no_of_box)
			return


	### Preparing Some data strucutres
	box1_lhs=""
	box1_rhs=""
	box2_lhs=""
	box2_rhs=""
	## Handle queries with 2 conditions
	if( len(a)>=15 and len(a[14])!=0):		
				flag=0
				condition1=a[10]
				condition2=a[14]
				if(no_of_box==1): ## Two conditions on same box
					second_box=first_box
				## Now process the condition 1
				if('.' in condition1==True): ## if table is explicitly mentioned
					tmp=condition1.split('.')
					table1_extracted=tmp[0].strip()
					condition1=tmp[1].strip()
					## find index 
					table1_extracted=convert_name_to_index(table1_extracted)
					## Match table_extracted with box1

					if(table1_extracted==first_box):
							condition1=condition1.split('=')
							box1_lhs=condition1[0].strip()
							box1_lhs=table_list[first_box].attributes.index(box1_lhs)
							box1_rhs=condition1[1].strip()	
						
							
					if(table1_extracted==second_box):
							condition1=condition1.split('=')
							box2_lhs=condition1[0].strip()
							box2_lhs=table_list[first_box].attributes.index(box2_lhs)
							box2_rhs=condition1[1].strip()

				else :    ## Tables not mentioned , Find attributes and tell which table

							condition1=condition1.split('=')
							attri=condition1[0].strip() ## Now search to which table this atri belongs
							
							## Search in box1
							try:
								x=table_list[first_box].attributes.index(attri) 
							except ValueError :
								x=-1
							if(x!= -1): ## Found in box1
								box1_lhs=attri
								box1_lhs=table_list[first_box].attributes.index(box1_lhs)
								box1_rhs=condition1[1].strip()

							## Search in box2
							if(first_box!=second_box):
								try:
									x=table_list[second_box].attributes.index(attri) 
								except ValueError :
										x=-1
								if(x!= -1): ## Found in box1
									box2_lhs=attri
									box2_lhs=table_list[first_box].attributes.index(box2_lhs)
									box2_rhs=condition1[1].strip()

				
				## Now process the condition 2
				if('.' in condition2==True): ## if table is explicitly mentioned
					tmp=condition2.split('.')
					table1_extracted=tmp[0].strip()
					condition2=tmp[1].strip()
					## find index 
					table1_extracted=convert_name_to_index(table1_extracted)
					## Match table_extracted with box1

					if(table1_extracted==first_box):
							condition2=condition2.split('=')
							box1_lhs=condition2[0].strip()
							box1_lhs=table_list[first_box].attributes.index(box1_lhs)
							box1_rhs=condition2[1].strip()	
						
							
					if(table1_extracted==second_box):
							condition2=condition2.split('=')
							box2_lhs=condition2[0].strip()
							box2_lhs=table_list[first_box].attributes.index(box2_lhs)
							box2_rhs=condition2[1].strip()

				else :    ## Tables not mentioned , Find attributes and tell which table
							condition2=condition2.split('=')
							attri=condition2[0].strip() ## Now search to which table this atri belongs
							
							## Search in box1
							if(first_box!=second_box):
								try:
									x=table_list[first_box].attributes.index(attri) 
								except ValueError :
									x=-1
								if(x!= -1): ## Found in box1
									box1_lhs=attri
									box1_lhs=table_list[first_box].attributes.index(box1_lhs)
									box1_rhs=condition2[1].strip()

							## Search in box2
							try:
								x=table_list[second_box].attributes.index(attri) 
							except ValueError :
									x=-1
							if(x!= -1): ## Found in box1
								box2_lhs=attri.strip()
								box2_lhs=table_list[second_box].attributes.index(box2_lhs)
								box2_rhs=condition2[1].strip()
				

				if (len(a[12])==3): ## AND is there
					product(first_box,second_box,box1_column,box2_column,box1_lhs,box1_rhs,box2_lhs,box2_rhs,3,no_of_box)
				if (len(a[12])==2): ## OR is  there 
					product(first_box,second_box,box1_column,box2_column,box1_lhs,box1_rhs,box2_lhs,box2_rhs,2,no_of_box)
	## Some more data strucutres
	box1_cond=""
	box2_cond=""

	## Join Conditions or Queries with 1 condition
	if(len(a)>=11 and len(a[10])!=0 and flag==1):
		## Checking for conditions
		y=0
		x=0
		tmp=a[10].split('=')
		if('.' in a[10]):
			tmp1=tmp[1].split('.')
			if(tmp1[1].isalpha() == True):
				y=1

		## Search for attributes in Condition
		abc=a[10]
		abc=abc.split('=')
		rh=abc[1].strip()
		if( rh.isdigit()==True or rh[0]=='-'):
			x=-1
		else:	
			## Search RHS in attributes
			try:
				x=table_list[first_box].attributes.index(abc[1].strip()) 
			except ValueError :
				x=-1
			try:
				x=table_list[second_box].attributes.index(abc[1].strip()) 
			except ValueError :
				x=-1

		if ( y==1 or x > -1 ) :		## If join , RHS will be an alphabet(Column name)
						flag=2
						condition=a[10]
						## Now process the conditions
						
						if('.' in condition): ## if table is explicitly mentioned
							tmp=condition.split('=')
							lhs=tmp[0]
							rhs=tmp[1]

							## Do lhs 
							lhs=lhs.split('.')
							table1_extracted=lhs[0].strip()
							## find index 
							table1_extracted=convert_name_to_index(table1_extracted)
							## Match table_extracted with box1

							if(table1_extracted==first_box):
								box1_cond=lhs[1].strip()
								x=table_list[first_box].attributes.index(box1_cond)
								box1_cond=x


							if(table1_extracted==second_box):
								box2_cond=lhs[1].strip()
								x=table_list[second_box].attributes.index(box2_cond)
								box2_cond=x

							## Do rhs
							rhs=rhs.split('.')
							table1_extracted=rhs[0].strip()
							## find index 
							table1_extracted=convert_name_to_index(table1_extracted)
							## Match table_extracted with box1

							if(table1_extracted==first_box):
								box1_cond=rhs[1].strip()
								x=table_list[first_box].attributes.index(box1_cond)
								box1_cond=x


							if(table1_extracted==second_box):
								box2_cond=rhs[1].strip()
								x=table_list[second_box].attributes.index(box2_cond)
								box2_cond=x
									
							

						else :   
						 ## Tables not mentioned , Find attributes and tell which table
									condition=a[10]

									tmp= condition.split('=')
									lhs=tmp[0]
									rhs=tmp[1]

									## Do lhs 
									lhs=lhs.strip()
									
									## Search in box1
									try:
										x=table_list[first_box].attributes.index(lhs) 
									except ValueError :
										x=-1
									if(x!= -1): ## Found in box1
										box1_cond=lhs
										box1_cond=table_list[first_box].attributes.index(box1_cond)

									## Search in box2 
									try:
										x=table_list[second_box].attributes.index(lhs) 
									except ValueError :
										x=-1
									if(x!= -1): ## Found in box1
										box2_cond=lhs
										box2_cond=table_list[second_box].attributes.index(box2_cond)

									## Do rhs
									rhs=rhs.strip()
									
									## Search in box1
									try:
										x=table_list[first_box].attributes.index(rhs) 
									except ValueError :
										x=-1
									if(x!= -1): ## Found in box1
										box1_cond=rhs
										box1_cond=table_list[first_box].attributes.index(box1_cond)

									## Search in box2 
									try:
										x=table_list[second_box].attributes.index(rhs) 
									except ValueError :
										x=-1
									if(x!= -1): ## Found in box1
										box2_cond=rhs
										box2_cond=table_list[second_box].attributes.index(box2_cond)
						join(first_box,second_box,box1_column,box2_column,box1_cond,box2_cond,flag,no_of_box)
						
		else :		## Normal condition (ONLY ONE)

			flag=3
			condition1=a[10]

			if('.' in condition1==True): ## if table is explicitly mentioned
					tmp=condition1.split('.')
					table1_extracted=tmp[0].strip()
					condition1=tmp[1].strip()
					## find index 
					table1_extracted=convert_name_to_index(table1_extracted)
					## Match table_extracted with box1

					if(table1_extracted==first_box):
							condition1=condition1.split('=')
							box1_lhs=condition1[0].strip()
							box1_lhs=table_list[first_box].attributes.index(box1_lhs)
							box1_rhs=condition1[1].strip()	
						

			else :    ## Tables not mentioned , Find attributes and tell which table
						condition1=condition1.split('=')
						attri=condition1[0].strip() ## Now search to which table this atri belongs
						
						## Search in box1
						try:
							x=table_list[first_box].attributes.index(attri) 
						except ValueError :
							x=-1
						if(x!= -1): ## Found in box1
							box1_lhs=attri
							box1_lhs=table_list[first_box].attributes.index(box1_lhs)
							box1_rhs=condition1[1].strip()
						product(first_box,second_box,box1_column,box2_column,box1_lhs,box1_rhs,box2_lhs,box2_rhs,0,no_of_box)
			

#### !!!! ###### Here The Program Begins ###########

#Set up the things before we begin
loc=input('Enter the Exact location of Database Files:\n')
# loc="/home/prakhar/Desktop/DBMS/Assignment1"
table_list=setup_tables(loc)
print("Enter EXIT to exit");
while(1) :

	sql=input('Enter the SQL Query:\n')
	# sql="select * from table1,table2 where  A=922  and D=5117"
	if(sql.lower() =='exit'):
		break

	sql=sql.replace('where','order') ## Because mysql parser doesnt recog where
	sql=sql.strip()
	query=sqlparse.parse(sql)
	tmp=query[0].tokens
	a=[]
	for i in range(len(tmp)):
		a.append(str(tmp[i]))

	if(len(a)<6):
		print('Please Enter Correct Query')
		continue
	parser()
