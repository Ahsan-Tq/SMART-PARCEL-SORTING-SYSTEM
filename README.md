# Smart Parcel Sorter

Hey guys! So I made this cool parcel tracking system for my school project. It's basically like those tracking apps you see online but simpler and made in Python!

## What is this?

So this is a parcel tracking system I built with Python. It has two parts:
- **userside.py** - where people can add parcels and track them
- **adminside.py** - where admins can manage all the parcels

## Features (the cool stuff!)

### Admin Side (the powerful one)
- Login system (pretty basic but works!)
- Can see all parcels in the system
- Can update parcel status (like when it's delivered)
- Can delete parcels if needed
- Can check for heavy parcels (over 10kg by default)
- Can search for specific parcels

### User Side (the simple one)
- Add new parcels with tracking numbers
- Track existing parcels
- See all parcels in the system
- Set priority levels (urgent, high, normal, low)

## How to install (super easy!)

### What you need:
- Python 3.6 or higher (I used Python 3.9)
- That's it! No extra packages needed

### Setup:
1. Download all the files
2. Put them in a folder called "SMART PARCEL SORTER"
3. Open terminal/command prompt in that folder
4. You're ready to go!

## How to use it

### Start the user side:
```bash
python userside.py
```

**Menu options:**
1. Add New Parcel
2. Track Parcel  
3. View All Parcels
4. Exit

### Start the admin side:
```bash
python adminside.py
```

**Login info:**
- Username: `admin` / Password: `admin123`
- Or Username: `manager` / Password: `manager123`

**Admin menu:**
1. View All Parcels
2. Update Parcel Status
3. Set Delivery Date
4. Delete Parcel
5. Check Heavy Parcels
6. Search Parcel
7. Logout
8. Exit

## How the parcel status works

Parcels go through these stages:
```
pending → in_transit → at_main_centre → out_for_delivery → delivered
```

**What each status means:**
- **pending**: Just created, waiting to be picked up
- **in_transit**: On the way to main center
- **at_main_centre**: At the sorting center
- **out_for_delivery**: Out for final delivery
- **delivered**: Successfully delivered!
- **returned**: If something went wrong

## How data is stored

The system uses a JSON file called `parcels.json` to store all the data. Both the user and admin sides can read and write to this file, so they stay in sync!

**File structure:**
```
SMART PARCEL SORTER/
├── userside.py          # User interface
├── adminside.py         # Admin interface  
├── parcels.json         # Data storage (created automatically)
└── README.md           # This file
```

## Priority levels

You can set different priorities for parcels:
1. **urgent** - Super important, gets processed first
2. **high** - Important, faster processing
3. **normal** - Regular priority (default)
4. **low** - Not urgent, standard processing

## Heavy parcel detection

The admin can check for heavy parcels (default is over 10kg). You can change this threshold if you want. Heavy parcels might need special handling!

## How I built this

### Classes I used:
- **Parcel** - stores all the parcel info
- **ParcelTracker** - manages parcels on user side
- **ParcelManager** - manages parcels on admin side
- **TrackingService** - generates tracking numbers
- **AdminApp** - handles admin interface
- **ParcelApp** - handles user interface

### Technologies:
- **Python** - the main language
- **JSON** - for storing data
- **datetime** - for dates and times
- **random** - for generating tracking numbers
- **os** - for file operations

## Example workflow

1. **User adds a parcel:**
   - Run `python userside.py`
   - Choose "Add New Parcel"
   - Enter details (weight, destination, sender, recipient)
   - Set priority
   - Get tracking number

2. **Admin manages the parcel:**
   - Run `python adminside.py`
   - Login with admin credentials
   - View all parcels
   - Update status as parcel moves through system
   - Set delivery date

3. **User tracks the parcel:**
   - Use tracking number to check status
   - See real-time updates from admin
   - Monitor delivery progress

## Troubleshooting (when things go wrong)

### Common problems:

**"File not found" errors:**
- Make sure you're in the right folder
- Check that both Python files are in the same directory

**Login issues:**
- Username: `admin` / Password: `admin123`
- Or Username: `manager` / Password: `manager123`
- Check for typos!

**Data not updating:**
- Make sure both interfaces can access `parcels.json`
- Check file permissions

### Error messages:
- **"Parcel not found"** - Tracking number doesn't exist
- **"Invalid credentials"** - Wrong username/password  
- **"Invalid input"** - Check your data format

## Future ideas (if I want to improve it)

Stuff I could add later:
- Web interface (would be cool!)
- Database instead of JSON files
- Email notifications when status changes
- Barcode/QR code scanning
- Analytics dashboard
- Multiple user accounts
- API for other systems

## License

This is open source so you can use it for school projects or whatever!

## Contributing

If you want to help improve this:
- Report bugs if you find any
- Suggest new features
- Help with documentation
- Add new functionality

## Support

If you have questions, check this README first. If you still need help, you can create an issue or ask around!

---

**Hope you like my parcel tracking system! It was fun to build! 🚀**

*P.S. This is my first big Python project, so be nice! 😅*
